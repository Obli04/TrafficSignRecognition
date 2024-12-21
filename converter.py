import os
import argparse
import yaml

def load_class_names(yaml_path):
    """Load class names from a YAML file."""
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
    return data.get('names', [])

def create_mapping(original_classes, grouped_classes):
    """
    Create a mapping from grouped class indices to lists of original class indices.

    Args:
        original_classes (list): List of original class names.
        grouped_classes (list): List of grouped class names.

    Returns:
        dict: A mapping from grouped class indices to lists of original class indices.
    """
    mapping = {i: [] for i in range(len(grouped_classes))}

    for idx, class_name in enumerate(original_classes):
        if "prohibitory" in class_name:
            mapping[grouped_classes.index("prohibitory")].append(idx)
        elif "danger" in class_name:
            mapping[grouped_classes.index("danger")].append(idx)
        elif "mandatory" in class_name:
            mapping[grouped_classes.index("mandatory")].append(idx)
        else:
            mapping[grouped_classes.index("other")].append(idx)

    return mapping

def process_label_file(file_path, mapping, output_dir):
    """
    Process a single label file, replacing class indices with grouped indices.

    Args:
        file_path (str): Path to the label file.
        mapping (dict): The mapping from grouped indices to original class indices.
        output_dir (str): Directory to save the updated label file.
    """
    output_path = os.path.join(output_dir, os.path.basename(file_path))
    with open(file_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            parts = line.strip().split()
            original_class = int(parts[0])

            # Find the grouped class index
            grouped_class = next((key for key, values in mapping.items() if original_class in values), None)
            if grouped_class is not None:
                outfile.write(f"{grouped_class} {' '.join(parts[1:])}\n")

def process_all_label_files(input_dir, output_dir, mapping):
    """
    Process all label files in the input directory.

    Args:
        input_dir (str): Directory containing the label files.
        output_dir (str): Directory to save the updated label files.
        mapping (dict): The mapping from grouped indices to original class indices.
    """
    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".txt"):
            process_label_file(os.path.join(input_dir, file_name), mapping, output_dir)

def main():
    parser = argparse.ArgumentParser(description="Map and replace label file class indices.")
    parser.add_argument("-oc", "--original_yaml", type=str, required=True, help="Path to the original YAML file.")
    parser.add_argument("-gc", "--grouped_yaml", type=str, required=True, help="Path to the grouped YAML file.")
    parser.add_argument("-i", "--input_dir", type=str, required=True, help="Path to the directory containing original label files.")
    parser.add_argument("-o", "--output_dir", type=str, required=True, help="Path to save the updated label files.")
    
    args = parser.parse_args()

    # Load class names from YAML files
    original_classes = load_class_names(args.original_yaml)
    grouped_classes = load_class_names(args.grouped_yaml)

    # Create the mapping
    mapping = create_mapping(original_classes, grouped_classes)

    # Process all label files
    process_all_label_files(args.input_dir, args.output_dir, mapping)
    print("Label files processed successfully.")

if __name__ == "__main__":
    main()
