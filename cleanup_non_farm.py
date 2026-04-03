import os
import re

# File with all monster IDs
all_monster_ids_file = "/home/georgegabor/all_monster_ids.txt"
spawns_dir = "/home/georgegabor/l2_final/game/data/spawns"

# List of files/folders to spare (NOT delete monsters from)
# Paths are relative to spawns_dir
SAFE_FILES = [
    "Goddard/VarkaSlenosOutpost.xml",
    "Goddard/KetraOrcOutpost.xml",
    "Goddard/GoddardMonsterSpawns.xml",
    "Goddard/ForgeOfTheGods.xml",
    "Goddard/ImperialTombMonsters.xml",
    "Goddard/WallOfArgos.xml",
    "Rune/PrimevalIsle.xml",
    "Rune/PaganTemple.xml",
    "Rune/SwampOfScreams.xml",
    "Giran/AntharasLair.xml",
    "Giran/DragonValey.xml",
    "Aden/TowerOfInsolenceMonsters.xml",
    "Aden/TowerOfInsolence.xml",
    "Aden/GiantsCave.xml",
    "Schuttgart/SchuttgartMonsterSpawns.xml"
]
# Also Goddard likely has more. We can just say any file in Goddard/ is safe.
SAFE_DRIS = ["Goddard"]

with open(all_monster_ids_file, "r") as f:
    monster_ids = set(line.strip() for line in f if line.strip())

print(f"Loaded {len(monster_ids)} monster IDs to target.")

id_pattern = re.compile(r'id="(\d+)"')

for root, dirs, files in os.walk(spawns_dir):
    # Check if directory is safe
    rel_dir = os.path.relpath(root, spawns_dir)
    is_safe_dir = any(rel_dir.startswith(safe_d) for safe_d in SAFE_DRIS)
    
    for filename in files:
        if filename.endswith(".xml"):
            rel_file = os.path.join(rel_dir, filename)
            if rel_file.startswith("./"):
                rel_file = rel_file[2:]
            
            if is_safe_dir or rel_file in SAFE_FILES:
                continue # Skip safe files
            
            filepath = os.path.join(root, filename)
            dirty = False
            new_lines = []
            
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            for line in lines:
                match = id_pattern.search(line)
                if match:
                    npc_id = match.group(1)
                    if npc_id in monster_ids:
                        dirty = True
                        continue # Skip (Delete)
                new_lines.append(line)
            
            if dirty:
                print(f"Cleaning {filepath}...")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)

print("Cleanup of non-farm monsters complete.")
