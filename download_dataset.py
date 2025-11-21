"""
Script to download and import Kaggle dataset.
Run this once to download the data.
"""
import kagglehub
import os
import shutil

# Download latest version
# path = kagglehub.dataset_download("akashunikaggle/steam-game-reviews-of-743-games")
path = kagglehub.dataset_download("baraazaid/pc-video-game-requirements")

print("Path to dataset files:", path)
print("\nFiles in dataset:")
for file in os.listdir(path):
    print(f"  - {file}")

# Copy files to local data directory
local_data_dir = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(local_data_dir, exist_ok=True)

print(f"\nCopying files to {local_data_dir}...")
for file in os.listdir(path):
    src = os.path.join(path, file)
    dst = os.path.join(local_data_dir, file)
    if os.path.isfile(src):
        shutil.copy2(src, dst)
        print(f"  ✓ Copied {file}")

print(f"\nDataset is now available in: {local_data_dir}")
