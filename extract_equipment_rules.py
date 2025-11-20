import json
import csv
from pathlib import Path

LOOT_ROOT = Path("minecraft_data/data/minecraft/loot_tables/entities/")
OUTPUT_EQUIP = Path("output/mob_equipment_rules.csv")

# Only mobs that can spawn with armor or items
ARMOR_CAPABLE_MOBS = {
    "zombie",
    "husk",
    "zombie_villager",
    "drowned",
    "skeleton",
    "stray",
    "wither_skeleton",
    "piglin",
    "piglin_brute",
    "vindicator",
    "pillager"
}

def guess_slot(item):
    if "helmet" in item: return "head"
    if "chestplate" in item: return "chest"
    if "leggings" in item: return "legs"
    if "boots" in item: return "feet"
    return None  # Other items (mainhand weapons) handled separately

def main():
    rows = []

    for loot_file in LOOT_ROOT.glob("*.json"):
        mob_id = loot_file.stem  # e.g., "zombie", "skeleton"

        if mob_id not in ARMOR_CAPABLE_MOBS:
            continue  # ❗Skip irrelevant mobs

        with open(loot_file, "r") as f:
            data = json.load(f)

        pools = data.get("pools", [])
        for pool in pools:
            entries = pool.get("entries", [])

            for entry in entries:
                # direct/weighted item
                if "name" in entry:
                    item = entry["name"].split(":")[1]
                    slot = guess_slot(item)
                    chance = entry.get("weight", 1)

                    if slot:
                        rows.append([mob_id, slot, item, chance])

                # functions for complex equipment rules
                for fn in entry.get("functions", []):
                    if fn.get("function") == "minecraft:set_contents":
                        for sub in fn.get("entries", []):
                            item = sub.get("name", "").split(":")[1]
                            slot = guess_slot(item)
                            chance = sub.get("weight", 1)

                            if slot:
                                rows.append([mob_id, slot, item, chance])

    OUTPUT_EQUIP.parent.mkdir(exist_ok=True)
    with open(OUTPUT_EQUIP, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["mob", "slot", "item", "chance"])
        writer.writerows(rows)

    print("✔ mob_equipment_rules.csv written")

if __name__ == "__main__":
    main()
