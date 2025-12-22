import os
import json

# --- CONFIGURATION ---
ICON_FOLDER = "xmas"  # Folder name containing images
OUTPUT_FILE = "bingo_map.json"

def create_manifest():
    if not os.path.exists(ICON_FOLDER):
        print(f"Error: Folder '{ICON_FOLDER}' not found.")
        return

    # Find all PNG files that start with a number
    files = [f for f in os.listdir(ICON_FOLDER) if f.endswith(".png") and f[0].isdigit()]
    files.sort()

    # Create the dictionary mapping { 1: "01_Coal.png", 2: "02_Santa.png" }
    data_map = {}
    
    print(f"Scanning '{ICON_FOLDER}'...")
    
    for filename in files:
        try:
            # Extract number from filename (e.g., "01" from "01_Coal.png")
            prefix = filename.split('_')[0]
            number = int(prefix)
            
            data_map[number] = filename
            print(f"  Mapped #{number} -> {filename}")
        except ValueError:
            print(f"  Skipping {filename} (could not parse number)")

    # Write to JSON file
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data_map, f, indent=2)

    print(f"\n✅ Success! Created '{OUTPUT_FILE}' with {len(data_map)} entries.")
    print("👉 ACTION: Upload this JSON file to your GitHub folder.")

if __name__ == "__main__":
    create_manifest();