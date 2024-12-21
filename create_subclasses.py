import os
import shutil
import yaml
import argparse

def load_yaml_classes(yaml_path):
    """Load class names from a YAML file."""
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
    return data['names']

def create_subset(input_dir, output_dir, classifier_yaml, subset_yaml, generic_yaml, subset_type, original_labels_dir):
    """
    Create a subset of the dataset containing only the specified signal type.

    Args:
        input_dir (str): Directory containing original dataset images and labels.
        output_dir (str): Directory where the subset will be created.
        classifier_yaml (str): Path to classifier YAML file.
        subset_yaml (str): Path to subset YAML file (e.g., prohibitory, danger, mandatory).
        generic_yaml (str): Path to generic YAML file.
        subset_type (str): Type of signals to extract (e.g., "prohibitory", "danger", "mandatory").
        original_labels_dir (str): Path to the original labels directory with classifier.yaml indices.
    """
    # Load class mappings from YAML files
    classifier_classes = load_yaml_classes(classifier_yaml)
    subset_classes = load_yaml_classes(subset_yaml)
    generic_classes = load_yaml_classes(generic_yaml)

    # Ensure output directory structure exists
    images_output_dir = os.path.join(output_dir, "images")
    labels_output_dir = os.path.join(output_dir, "labels")
    os.makedirs(images_output_dir, exist_ok=True)
    os.makedirs(labels_output_dir, exist_ok=True)

    # Map classifier indices to subset indices
    classifier_to_subset = {
        classifier_classes.index(class_name): subset_classes.index(class_name)
        for class_name in subset_classes
    }

    # Process each label file in the input directory
    labels_input_dir = os.path.join(input_dir, "labels")
    for label_file in os.listdir(labels_input_dir):
        if not label_file.endswith(".txt"):
            continue

        label_path = os.path.join(labels_input_dir, label_file)
        original_label_path = os.path.join(original_labels_dir, label_file)
        output_label_path = os.path.join(labels_output_dir, label_file)

        with open(label_path, 'r') as infile, open(original_label_path, 'r') as original_labels, open(output_label_path, 'w') as outfile:
            original_lines = original_labels.readlines()
            image_contains_subset = False

            for line in infile:
                parts = line.strip().split()
                generic_class_index = int(parts[0])

                if generic_classes[generic_class_index] == subset_type:
                    # Find the matching line in the original labels
                    matching_line = next((line for line in original_lines if line.strip().split()[1:] == parts[1:]), None)

                    if matching_line:
                        classifier_index = int(matching_line.strip().split()[0])
                        subset_index = classifier_to_subset.get(classifier_index, None)

                        if subset_index is not None:
                            outfile.write(f"{subset_index} {' '.join(parts[1:])}\n")
                            image_contains_subset = True

            # If no relevant labels remain, remove the label file
            if not image_contains_subset:
                os.remove(output_label_path)

        # Copy corresponding image if it contains relevant signals
        if image_contains_subset:
            image_file = label_file.replace(".txt", ".jpg")
            image_path = os.path.join(input_dir, "images", image_file)
            if os.path.exists(image_path):
                shutil.copy(image_path, images_output_dir)

def main():
    parser = argparse.ArgumentParser(description="Create a subset from the dataset for a specific signal type.")
    parser.add_argument("-i", type=str, required=True, help="Path to the input dataset directory.")
    parser.add_argument("-o", type=str, required=True, help="Path to the output subset directory.")
    parser.add_argument("-c", type=str, required=True, help="Path to the classifier YAML file.")
    parser.add_argument("-s", type=str, required=True, help="Path to the subset YAML file (e.g., prohibitory, danger, mandatory).")
    parser.add_argument("-g", type=str, required=True, help="Path to the generic YAML file.")
    parser.add_argument("-t", type=str, required=True, choices=["prohibitory", "danger", "mandatory", "other"], help="Type of signals to extract.")
    parser.add_argument("-og", type=str, required=True, help="Path to the original labels directory with classifier.yaml indices.")
    args = parser.parse_args()

    create_subset(
        input_dir=args.i,
        output_dir=args.o,
        classifier_yaml=args.c,
        subset_yaml=args.s,
        generic_yaml=args.g,
        subset_type=args.t,
        original_labels_dir=args.og
    )

if __name__ == "__main__":
    main()
