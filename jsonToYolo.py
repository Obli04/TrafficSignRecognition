import json
import os
import yaml

# Paths to directories and files
ANNOTATIONS_DIR = 'mtsd_v2_fully_annotated/annotations'
SPLITS_DIR = 'mtsd_v2_fully_annotated/splits'
OUTPUT_BASE_DIRS = {
    'train': 'datasets/training/labels',
    'val': 'datasets/evaluation/labels',
    'test': 'datasets/test/labels'
}
CLASSIFIER_YAML = 'classifier2.yaml'

# Load class mappings from the classifier yaml file
try:
    with open(CLASSIFIER_YAML, 'r') as f:
        classifier_config = yaml.safe_load(f)
    class_names = classifier_config.get('names', []) #Extract the list of class names
    class_mapping = {name.strip('-'): idx for idx, name in enumerate(class_names)} #Create a dictionary mapping class names to their indexes
except Exception as e:
    raise e

# Read split files and create sets for quick lookup
def load_split_ids(split_file_path): #Split the files into train, val and test
    try:
        with open(split_file_path, 'r') as f: 
            split_ids = set(line.strip() for line in f if line.strip())  # Read each line, remove whitespace, and add to a set if the line is not empty
        return split_ids
    except Exception as e:
        return set()

#Load the ids of the train, val and test files
train_ids = load_split_ids(os.path.join(SPLITS_DIR, 'train.txt'))
val_ids = load_split_ids(os.path.join(SPLITS_DIR, 'val.txt'))
test_ids = load_split_ids(os.path.join(SPLITS_DIR, 'test.txt'))


for split, dir_path in OUTPUT_BASE_DIRS.items():
    os.makedirs(dir_path, exist_ok=True) #Make sure the folder exists

# Process each annotation file
for filename in os.listdir(ANNOTATIONS_DIR):
    if not filename.endswith('.json'):
        continue

    file_id = os.path.splitext(filename)[0] #Get the file id by removing the extension
    annotation_path = os.path.join(ANNOTATIONS_DIR, filename) #Get the path to the annotation file

    # Determine where the file belongs
    if file_id in train_ids:
        split = 'train'
    elif file_id in val_ids:
        split = 'val'
    elif file_id in test_ids:
        split = 'test'
    else:
        continue

    output_dir = OUTPUT_BASE_DIRS[split] #Get the output directory
    output_file = os.path.join(output_dir, f"{file_id}.txt") #Get the path to the output file

    # Load JSON annotation
    with open(annotation_path, 'r') as f:
        annotation = json.load(f)

    #Get the objects in the annotation
    objects = annotation.get('objects', [])
    #Get the width and height of the image
    image_width = annotation.get('width', None)
    image_height = annotation.get('height', None)

    if image_width is None or image_height is None: #If the width or height is not found, skip the file
        continue

    if image_width <= 0 or image_height <= 0: #If the width or height is not found, skip the file
        continue

    yolo_annotations = [] #Initialize the list of YOLO annotations
    for obj in objects:
        class_name = obj.get('label', '').strip('-') #Get the class name
        class_id = class_mapping[class_name] #Get the class id

        #Get all the bounding box coordinates
        bbox = obj.get('bbox', {})
        xmin = bbox.get('xmin', None)
        ymin = bbox.get('ymin', None)
        xmax = bbox.get('xmax', None)
        ymax = bbox.get('ymax', None)
        
        # Calculate normalized coordinates for resized image (20% of original size)
        resized_width = image_width * 0.2
        resized_height = image_height * 0.2
        x_center = ((xmin + xmax) / 2) / resized_width
        y_center = ((ymin + ymax) / 2) / resized_height
        bbox_width = (xmax - xmin) / resized_width
        bbox_height = (ymax - ymin) / resized_height

        yolo_annotations.append(f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}") #Write the YOLO annotation to the file

    with open(output_file, 'w') as out_f:
        out_f.write('\n'.join(yolo_annotations)) #Write the YOLO annotations to the file