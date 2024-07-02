import random
import csv

focus_areas = ["Focus Area 1", "Focus Area 2", "Focus Area 3", "Focus Area 4"]
risk_levels = ["Low", "Medium", "High"]
tiers = ["Tier 1", "Tier 2", "Tier 3"]
data_filename = "output.csv"
metrics_filename = "metrics_report.csv"

# Number of record comments to write to the file
N = 10

def generate_focus_area(type):
    count = random.randint(1, len(focus_areas))
    focus_str = []
    metrics = []

    for _ in range(count):
        focus = random.choice(focus_areas)
        risk = random.choice(risk_levels)
        tier = random.choice(tiers) if type in ["SHM", "MHM"] else ""

        if type in ["SHM", "MHM"]:
            focus_str.append(f"{focus} – {tier} - (Risk Level {risk})")
            metrics.append([focus, risk, tier])
        else:
            focus_str.append(f"{focus} (Risk Level {risk})")
            metrics.append([focus, risk, ""])  # No tier

    return ", ".join(focus_str), metrics

def generate_smart_comment(record_id):
    types = ["INF", "SHM", "MHM", "CAA", "OPM", "AEM"]
    random.shuffle(types)
    comment = "SMART - "
    all_metrics = []

    for type in types:
        focus_area_string, metrics = generate_focus_area(type)
        comment += f"SMART ({type}): {focus_area_string}. "
        for metric in metrics:
            all_metrics.append([record_id, type] + metric + ['True'])  # Adding 'True' for the 'Valid' column

    return comment.strip(), all_metrics

with open(data_filename, "w", newline='', encoding='utf-8') as data_file, \
     open(metrics_filename, "w", newline='', encoding='utf-8') as metrics_file:
    data_writer = csv.writer(data_file)
    metrics_writer = csv.writer(metrics_file)
    data_writer.writerow(["Record ID", "SMART Record Comment"])
    metrics_writer.writerow(["Record ID", "Type", "Focus Area", "Risk Level", "Tier", "Valid"])

    for _ in range(N):
        record_id = random.randint(1000, 9999)
        comment, metrics = generate_smart_comment(record_id)
        data_writer.writerow([record_id, comment])
        metrics_writer.writerows(metrics)

print("Data generation and metrics recording complete.")
