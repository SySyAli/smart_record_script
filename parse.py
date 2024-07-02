import csv
import re

input_file = "output.csv"
output_file = "parsed_output.csv"

def validate_entry(entry):
    # check if record id exists
    id_valid = entry[0] is not None
    type_valid = entry[1] in ['INF', 'SHM', 'MHM', 'CAA', 'OPM', 'AEM']
    focus_area_valid = bool(entry[2].strip())
    risk_level_valid = entry[3] in ['Low', 'Medium', 'High']
    tier_valid = entry[4] in ['1', '2', '3']
    print(entry, type_valid, focus_area_valid, risk_level_valid, tier_valid)
    if entry[1] in ['SHM', 'MHM']:
        return id_valid and type_valid and focus_area_valid and risk_level_valid and tier_valid
    else:
        return id_valid and type_valid and focus_area_valid and risk_level_valid

def parse_general(entry):
    # Adjusting regex for general types without tier information
    match = re.match(r"([^\(\)\-–]+)\s*\(\s*Risk\s*Level\s*(Low|Medium|High)\s*\)?", entry.strip())
    if match:
        focus_area, risk_level = match.groups()
        return focus_area.strip(), '', risk_level.strip()
    return None, None, None

def parse_shm_mhm(entry):
    # Updated regex to handle flexible whitespaces and optional dashes around 'Tier'
    match = re.match(r"([^\(\)\-–]+)\s*[-–]\s*Tier\s*([1-3])\s*[-–]?\s*\(\s*Risk\s*Level\s*(Low|Medium|High)\s*\)?", entry.strip())
    if match:
        focus_area, tier, risk_level = match.groups()
        return focus_area.strip(), tier.strip(), risk_level.strip()
    return None, None, None

def parse_comment(record_id, comment):
    parsed_data = []
    pattern = r"SMART \((INF|SHM|MHM|CAA|OPM|AEM)\): (.*?)(?=\s*SMART \((INF|SHM|MHM|CAA|OPM|AEM)\)|$)"
    matches = re.findall(pattern, comment, re.DOTALL)

    for match in matches:
        current_type = match[0]
        content = match[1]

        entries = re.split(r"\),?\s*", content.strip('.'))
        for entry in entries:
            if current_type in ['SHM', 'MHM']:
                focus_area, tier, risk_level = parse_shm_mhm(entry)
            else:
                focus_area, tier, risk_level = parse_general(entry)

            if focus_area and risk_level:
                entry_data = [record_id, current_type, focus_area, risk_level, tier]
                is_valid = 'True' if validate_entry(entry_data) else 'False'
                entry_data.append(is_valid)
                parsed_data.append(entry_data)
            else:
                print(f"Failed to parse entry: {current_type} {entry}")

    return parsed_data

# Reading and writing CSV
with open(input_file, mode='r', newline='', encoding='utf-8') as file, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(file)
    writer = csv.writer(outfile)
    writer.writerow(['Record ID', 'Type', 'Focus Area', 'Risk Level', 'Tier', 'Valid'])

    next(reader)  # Skip header if present
    for row in reader:
        record_id = row[0]
        comment = row[1]
        parsed_comments = parse_comment(record_id, comment)
        for data in parsed_comments:
            writer.writerow(data)

print("CSV parsing complete. Output file created with data integrity checks.")
