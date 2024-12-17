import os
import pandas as pd
import shutil

# === PARAMETRI ===
IMAGES_PATH = "Final_Training/Images"  # Cartella principale con tutte le classi
OUTPUT_PATH = "GTSRB_YOLO"  # Cartella di output YOLO
TRAIN_RATIO = 0.8  # Percentuale di dati per il training

# === FUNZIONI ===

def convert_to_yolo(x1, y1, x2, y2, width, height):
    """Converte bounding box in formato YOLO."""
    x_center = (x1 + x2) / 2 / width
    y_center = (y1 + y2) / 2 / height
    bbox_width = (x2 - x1) / width
    bbox_height = (y2 - y1) / height
    return x_center, y_center, bbox_width, bbox_height

def process_gtsrb(images_path, output_path, train_ratio):
    """Converte il dataset GTSRB in formato YOLO."""
    os.makedirs(output_path, exist_ok=True)
    train_images = os.path.join(output_path, "train/images")
    train_labels = os.path.join(output_path, "train/labels")
    val_images = os.path.join(output_path, "val/images")
    val_labels = os.path.join(output_path, "val/labels")

    for dir in [train_images, train_labels, val_images, val_labels]:
        os.makedirs(dir, exist_ok=True)

    
    class_dirs = [d for d in os.listdir(images_path) if os.path.isdir(os.path.join(images_path, d))]

    all_data = []

    for class_dir in class_dirs:
        class_path = os.path.join(images_path, class_dir)
        csv_file = os.path.join(class_path, f"GT-{class_dir}.csv")

        if not os.path.isfile(csv_file):
            print(f"⚠️ File CSV non trovato in: {csv_file}")
            continue

       
        data = pd.read_csv(csv_file, sep=";")
        data['class_dir'] = class_dir  
        all_data.append(data)


    full_data = pd.concat(all_data, ignore_index=True)


    full_data = full_data.sample(frac=1, random_state=42).reset_index(drop=True)
    split_idx = int(len(full_data) * train_ratio)
    train_data = full_data[:split_idx]
    val_data = full_data[split_idx:]


    for split, split_data in [("train", train_data), ("val", val_data)]:
        for _, row in split_data.iterrows():
            filename = row['Filename']
            width, height = row['Width'], row['Height']
            x1, y1, x2, y2 = row['Roi.X1'], row['Roi.Y1'], row['Roi.X2'], row['Roi.Y2']
            class_id = row['ClassId']
            class_dir = row['class_dir']  

 
            x_center, y_center, bbox_width, bbox_height = convert_to_yolo(x1, y1, x2, y2, width, height)

     
            label_filename = os.path.splitext(filename)[0] + ".txt"
            label_path = os.path.join(output_path, split, "labels", label_filename)
            with open(label_path, 'w') as f:
                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}\n")

 
            img_src = os.path.join(images_path, class_dir, filename)
            img_dst = os.path.join(output_path, split, "images", filename)
            try:
                shutil.copy(img_src, img_dst)
            except FileNotFoundError:
                print(f"Image not found: {img_src}")
    
    print("Done")

# === SCRIPT PRINCIPALE ===
if __name__ == "__main__":
    process_gtsrb(IMAGES_PATH, OUTPUT_PATH, TRAIN_RATIO)
