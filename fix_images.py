import os
import json
from PIL import Image, ImageFilter

def process_images():
    # Configuration
    input_folder = 'xmas'
    output_folder = 'processed_xmas_icons'
    target_size = (1024, 1024)  # Enlarge all icons to this size
    
    # Create output directory
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    # Load the bingo map to get the list of files
    map_path = os.path.join(input_folder, 'bingo_map.json')
    try:
        with open(map_path, 'r') as f:
            bingo_map = json.load(f)
        files = list(bingo_map.values())
        print(f"Loaded map with {len(files)} entries.")
    except FileNotFoundError:
        print(f"Could not find {map_path}. Processing all PNGs in {input_folder} instead.")
        files = [f for f in os.listdir(input_folder) if f.lower().endswith('.png')]

    print("Starting processing...")

    for filename in files:
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        # Check if file exists (skipping iCloud placeholders)
        if not os.path.exists(input_path):
            print(f"Skipping missing file: {filename} (Check if it is an .icloud placeholder)")
            continue
            
        try:
            with Image.open(input_path) as img:
                # Convert to RGBA to preserve transparency
                img = img.convert("RGBA")
                
                # Resize using LANCZOS for high quality upscaling
                img_resized = img.resize(target_size, resample=Image.LANCZOS)
                
                # Apply Unsharp Mask to fix blurriness
                # Radius=2 and Percent=150 are good starting values for upscaled icons
                img_sharpened = img_resized.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
                
                # Save the processed image
                img_sharpened.save(output_path)
                print(f"Processed: {filename}")
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print("\nProcessing complete! Check the folder:", output_folder)

if __name__ == "__main__":
    process_images()