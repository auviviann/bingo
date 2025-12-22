import os
import random
import re

# --- CONFIGURATION ---
FOLDER_PATH = "xmas"
FREE_SPACE_FILE = "free_space_tree.png"

def clean_filename(filename):
    """
    Removes existing number prefixes like '01_' or '55_' so we don't 
    get files named '01_05_santa.png' if you run the script twice.
    """
    # Regex checks if file starts with 2 digits and an underscore (e.g., "01_")
    if re.match(r'^\d{2}_', filename):
        return filename[3:] # Remove the first 3 characters
    return filename

def randomize_and_rename():
    # 1. Check if folder exists
    if not os.path.exists(FOLDER_PATH):
        print(f"Error: Folder '{FOLDER_PATH}' not found.")
        return

    # 2. Get all PNG files except the free space
    files = [f for f in os.listdir(FOLDER_PATH) 
             if f.endswith(".png") and f != FREE_SPACE_FILE]

    if not files:
        print("No PNG files found to rename.")
        return

    print(f"Found {len(files)} files. Shuffling and renaming...")

    # 3. Shuffle the list randomly
    random.shuffle(files)

    # 4. Rename files
    # We use a temporary rename step to avoid collisions 
    # (e.g., trying to rename A to B, when B already exists)
    
    # Step A: Rename everything to a temporary random name
    temp_map = []
    for filename in files:
        # Generate a clean base name (remove old numbers if they exist)
        clean_name = clean_filename(filename)
        
        # Create a temp name
        temp_name = f"temp_{random.randint(10000,99999)}_{clean_name}"
        
        old_path = os.path.join(FOLDER_PATH, filename)
        temp_path = os.path.join(FOLDER_PATH, temp_name)
        
        os.rename(old_path, temp_path)
        temp_map.append((temp_name, clean_name))

    # Step B: Rename from temp to final numbered name
    for index, (temp_name, original_clean_name) in enumerate(temp_map):
        # Format number with leading zero (01, 02, ... 80)
        number_prefix = f"{index + 1:02d}"
        new_filename = f"{number_prefix}_{original_clean_name}"
        
        temp_path = os.path.join(FOLDER_PATH, temp_name)
        final_path = os.path.join(FOLDER_PATH, new_filename)
        
        os.rename(temp_path, final_path)
        print(f"Renamed: {original_clean_name} -> {new_filename}")

    print("\n✅ Renaming complete!")
    print(f"Total files numbered: {len(files)}")

if __name__ == "__main__":
    randomize_and_rename()