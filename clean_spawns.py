import os
import re

junk_ids_file = "/home/georgegabor/junk_monster_ids.txt"
spawns_dir = "/home/georgegabor/l2_final/game/data/spawns"

with open(junk_ids_file, "r") as f:
    junk_ids = set(line.strip() for line in f if line.strip())

print(f"Loaded {len(junk_ids)} junk IDs.")

id_pattern = re.compile(r'id="(\d+)"')

for root, dirs, files in os.walk(spawns_dir):
    for filename in files:
        if filename.endswith(".xml"):
            filepath = os.path.join(root, filename)
            dirty = False
            new_lines = []
            
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            for line in lines:
                match = id_pattern.search(line)
                if match:
                    npc_id = match.group(1)
                    if npc_id in junk_ids:
                        dirty = True
                        continue # Skip this line (deleting the spawn)
                new_lines.append(line)
            
            if dirty:
                print(f"Cleaning {filepath}...")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)

print("Cleanup complete.")
