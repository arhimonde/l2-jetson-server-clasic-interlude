import os
import re
import random

npcs_dir = "/home/georgegabor/l2_final/game/data/stats/npcs/"
spawns_dir = "/home/georgegabor/l2_final/game/data/spawns/"

# Farm Zones mapped to levels
ZONES = {
    80: [
        "Goddard/KetraOrcOutpost.xml", 
        "Goddard/VarkaSlenosOutpost.xml", 
        "Giran/AntharasLair.xml", 
        "Giran/DragonValey.xml", 
        "Rune/PrimevalIsle.xml",
        "Rune/SwampOfScreams.xml"
    ],
    85: [
        "Goddard/ImperialTombMonsters.xml",
        "Rune/PaganTemple.xml",
        "Aden/TowerOfInsolenceMonsters.xml",
        "Aden/GiantsCave.xml"
    ],
    90: [
        "Goddard/ForgeOfTheGods.xml",
        "Goddard/WallOfArgos.xml",
        "Schuttgart/SchuttgartMonsterSpawns.xml"
    ]
}

def get_raid_bosses():
    rb_list = []
    npc_pattern = re.compile(r'<npc id="(\d+)" level="(\d+)" type="RaidBoss" name="([^"]+)"')
    for root, dirs, files in os.walk(npcs_dir):
        for f in files:
            if f.endswith(".xml"):
                with open(os.path.join(root, f), "r", encoding="utf-8") as file:
                    content = file.read()
                    matches = npc_pattern.findall(content)
                    for m in matches:
                        rb_list.append({'id': m[0], 'level': int(m[1]), 'name': m[2]})
    return rb_list

def get_random_coords(zone_path):
    # For now, we use a central point for each area, but ideally we'd want random variations
    # We'll use the coordinates we already have for cities/zones as base
    COORDS = {
        "Goddard/KetraOrcOutpost.xml": (139450, -44630, -2734),
        "Goddard/VarkaSlenosOutpost.xml": (108450, -44630, -2734),
        "Giran/AntharasLair.xml": (131238, 114407, -3726),
        "Giran/DragonValey.xml": (110444, 110444, -3701),
        "Rune/PrimevalIsle.xml": (11150, -24100, -2700),
        "Rune/SwampOfScreams.xml": (80450, -11630, -2734),
        "Goddard/ImperialTombMonsters.xml": (181450, -11630, -2734),
        "Rune/PaganTemple.xml": (-15100, -15200, -2200),
        "Aden/TowerOfInsolenceMonsters.xml": (114223, 15805, -3132),
        "Aden/GiantsCave.xml": (181400, 55400, -2734),
        "Goddard/ForgeOfTheGods.xml": (187450, -135430, -2734),
        "Goddard/WallOfArgos.xml": (187450, -44630, -2734),
        "Schuttgart/SchuttgartMonsterSpawns.xml": (85386, -145246, -1293)
    }
    base = COORDS.get(zone_path, (0, 0, 0))
    # Add random jitter to avoid stacking
    return (base[0] + random.randint(-500, 500), base[1] + random.randint(-500, 500), base[2])

bosses = get_raid_bosses()
print(f"Found {len(bosses)} Raid Bosses.")

for rb in bosses:
    target_lvl = 80
    if rb['level'] > 85: target_lvl = 90
    elif rb['level'] > 80: target_lvl = 85
    
    zone_file = random.choice(ZONES[target_lvl])
    filepath = os.path.join(spawns_dir, zone_file)
    x, y, z = get_random_coords(zone_file)
    
    # Append to file before </list>
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "</list>" in content:
        spawn_entry = f'    <spawn name="RedistributedRaid"><npc id="{rb["id"]}" x="{x}" y="{y}" z="{z}" heading="0" respawnTime="7200sec"/></spawn>\n</list>'
        content = content.replace("</list>", spawn_entry)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

print("Redistribution complete.")
