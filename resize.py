from PIL import Image
import os
import sys

def resize_images(input_folder, scale_percent=20):
    if not os.path.exists(input_folder):
        print(f"Error: Folder '{input_folder}' does not exist")
        return

    #Get all files in the directory
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    total_images = len(image_files) #I get the total amount of images to print the progress
    
    if not total_images:
        print("No images found to resize.")
        return

    scale_factor = scale_percent / 100
    #Loop through each image file in the directory, keeping track of the index and filename
    for index, filename in enumerate(image_files):
        input_path = os.path.join(input_folder, filename) #Construct the full path to the image file
        
        try:
            with Image.open(input_path) as img: #Open the image and calculate the new dimensions (width and height)
                width = int(img.size[0] * scale_factor)
                height = int(img.size[1] * scale_factor)

                resized_img = img.resize((width, height), Image.Resampling.LANCZOS) #Resize the image using the calculated dimensions
                
                resized_img.save(input_path, quality=100, optimize=True) #Save the resized image with maximum quality
            
            progress = (index + 1) / total_images * 100 #Calculate and print progress
            sys.stdout.write(f"\rProgress: {progress:.2f}% - Resized {filename}")
            sys.stdout.flush()
        
        except Exception as e:
            print(f"\nError processing {filename}: {str(e)}")

if __name__ == "__main__":
    eval_folder = os.path.join("Models", "evaluation", "images") #Paths to the folders to resize
    train_folder = os.path.join("Models", "training", "images")
    test_folder = os.path.join("Models", "test", "images")
    resize_images(eval_folder, scale_percent=20)
    resize_images(train_folder, scale_percent=20)
    resize_images(test_folder, scale_percent=20)