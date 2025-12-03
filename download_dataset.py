"""
Script to download and import Kaggle dataset.
Run this once to download the data.
"""
import kagglehub
import os
import shutil

# Local data directory
local_data_dir = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(local_data_dir, exist_ok=True)

# Define datasets with their expected output filenames
datasets = [
    {
        "name": "akashunikaggle/steam-game-reviews-of-743-games",
        "file_mapping": {
            "steam_game_reviews.csv": "steam_game_reviews.csv"
        }
    },
    {
        "name": "baraazaid/pc-video-game-requirements",
        "file_mapping": {
            # Map whatever filename to the expected name
            "*.csv": "pc_videogame_requirements.csv"  # Will rename any CSV file
        }
    },
    {
        "name": "fronkongames/steam-games-dataset",
        "file_mapping": {
            "games.csv": "games.csv",
            "games.json": "games.json"
        }
    }
]

for dataset_info in datasets:
    dataset = dataset_info["name"]
    print(f"\nDownloading {dataset}...")
    path = kagglehub.dataset_download(dataset)
    print(f"Path to dataset files: {path}")
    
    print(f"Files in dataset:")
    files = os.listdir(path)
    for file in files:
        print(f"  - {file}")
    
    print(f"Copying files to {local_data_dir}...")
    
    # Handle file mapping
    file_mapping = dataset_info["file_mapping"]
    for pattern, target_name in file_mapping.items():
        if pattern == "*.csv":
            # Find any CSV file and rename it
            csv_files = [f for f in files if f.endswith('.csv')]
            if csv_files:
                src = os.path.join(path, csv_files[0])
                dst = os.path.join(local_data_dir, target_name)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                    print(f"  ✓ Copied {csv_files[0]} → {target_name}")
        else:
            # Direct file mapping
            if pattern in files:
                src = os.path.join(path, pattern)
                dst = os.path.join(local_data_dir, target_name)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                    print(f"  ✓ Copied {pattern}" + (f" → {target_name}" if pattern != target_name else ""))

print(f"\n✅ All datasets are now available in: {local_data_dir}")
print(f"\nExpected files:")
print(f"  - steam_game_reviews.csv")
print(f"  - games.csv")
print(f"  - games.json")
print(f"  - pc_videogame_requirements.csv")
