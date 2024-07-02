import random
import csv
# TODO: FIGURE OUT WAY TO KEEP TRACK OF EVERYTHING GENERATED
focus_areas = ["Focus Area 1", "Focus Area 2", "Focus Area 3", "Focus Area 4"]
risk_levels = ["Low", "Medium", "High"]
tiers = ["Tier 1", "Tier 2", "Tier 3"]
filename = "output.csv"
# number of record comments to write to the file
N = 10

def generate_focus_area(type):
    count = random.randint(1, len(focus_areas))
    focus_str = []
    # current combination - (INF, SHM, MHM, CAA, OPM, AEM)
    # INF, CAA, OPM, AEM only have a Risk Level
    # SHM, MHM both have a Tier and Risk Level
    for _ in range(count):
        if type == "INF":
            focus_str.append(f"{random.choice(focus_areas)} (Risk Level {random.choice(risk_levels)})")
        elif type == "CAA":
            focus_str.append(f"{random.choice(focus_areas)} (Risk Level {random.choice(risk_levels)})")
        elif type == "AEM":
            focus_str.append(f"{random.choice(focus_areas)} (Risk Level {random.choice(risk_levels)})")
        elif type == "OPM":
            focus_str.append(f"{random.choice(focus_areas)} (Risk Level {random.choice(risk_levels)})")
        elif type == "SHM":
            focus_str.append(f"{random.choice(focus_areas)} – {random.choice(tiers)} - (Risk Level {random.choice(risk_levels)})")
        elif type == "MHM":
            focus_str.append(f"{random.choice(focus_areas)} – {random.choice(tiers)} - (Risk Level {random.choice(risk_levels)})")
    return ", ".join(focus_str)

def generate_smart_comment():
    sections = ["INF", "SHM", "MHM", "CAA", "OPM", "AEM"]
    random.shuffle(sections)
    comment = "SMART - "
    comment += ". ".join([f"SMART ({sec}): {generate_focus_area(sec)}" for sec in sections])
    comment += "."
    return comment


# for _ in range(10):
#     print(generate_smart_comment())

with open(filename, "w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Record ID", "SMART Record Comment"])
    for _ in range(N):
        # generate a random id for the record
        record_id = random.randint(1000, 9999)
        writer.writerow([record_id, generate_smart_comment()])
