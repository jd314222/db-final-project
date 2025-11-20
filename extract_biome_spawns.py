import json
import csv
from pathlib import Path

# ----------------------------
# CONFIG PATHS
# ----------------------------
DATA_ROOT = Path(
    "/home/eeisnaugle/CS3620/db-final-project/minecraft_version_data_unzipped/data/minecraft/worldgen/biome"
)

OUTPUT_SPAWN_CSV = Path("output/mob_spawn_rules.csv")
OUTPUT_BIOME_CSV = Path("output/biome_list.csv")

# ----------------------------
# MOBS WE CARE ABOUT
# (Only mobs that can spawn with armor or weapons)
# ----------------------------
EQUIPPABLE_MOBS = {
    "zombie",
    "husk",
    "drowned",
    "zombie_villager",
    "skeleton",
    "stray",
    "wither_skeleton",
    "piglin",
    "piglin_brute",
    "zombified_piglin",
    "vindicator",
    "pillager"
}


def extract_spawn_rules():
    spawn_rows = []
    biome_rows = []

    if not DATA_ROOT.exists():
        print("ERROR: DATA_ROOT does not exist:", DATA_ROOT)
        return

    for biome_file in DATA_ROOT.glob("*.json"):
        biome_id = biome_file.stem  # filename without extension
        biome_rows.append([biome_id])

        with open(biome_file, "r") as f:
            biome_data = json.load(f)

        # -----------------------------------------------
        # Minecraft 1.19+ uses top-level "spawners"
        # but older versions sometimes place it under "spawn"
        # -----------------------------------------------
        spawners = biome_data.get("spawners", {})

        # Fallback (older schema)
        if not spawners or not isinstance(spawners, dict):
            spawn_block = biome_data.get("spawn", {})
            spawners = spawn_block.get("spawners", {})

        # If still nothing, skip biome
        if not isinstance(spawners, dict):
            continue

        # Only process monster category
        monster_entries = spawners.get("monster", [])
        if not monster_entries:
            continue  # skip biomes without hostile mobs

        # -----------------------------------------------
        # Extract each equipable mob spawn rule
        # -----------------------------------------------
        for entry in monster_entries:
            mob_type = entry.get("type", "")
            if mob_type.startswith("minecraft:"):
                mob_type = mob_type.split(":")[1]

            # Filter ONLY equipable mobs
            if mob_type not in EQUIPPABLE_MOBS:
                continue

            spawn_rows.append([
                biome_id,
                "monster",
                mob_type,
                entry.get("weight", 0),
                entry.get("minCount", 0),
                entry.get("maxCount", 0)
            ])

    # -----------------------------------------------
    # Output CSVs
    # -----------------------------------------------
    OUTPUT_SPAWN_CSV.parent.mkdir(exist_ok=True)

    # Biome list
    with open(OUTPUT_BIOME_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["biome_id"])
        writer.writerows(biome_rows)

    # Spawn rules
    with open(OUTPUT_SPAWN_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["biome_id", "category", "mob", "weight", "min_count", "max_count"])
        writer.writerows(spawn_rows)

    print("✔ biome_list.csv written -->", OUTPUT_BIOME_CSV)
    print("✔ mob_spawn_rules.csv written -->", OUTPUT_SPAWN_CSV)


if __name__ == "__main__":
    extract_spawn_rules()
