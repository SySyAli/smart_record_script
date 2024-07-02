# For PowerBI use
import pandas as pd
import re

def validate_entry(entry):
    # check if record id exists
    id_valid = entry[0] is not None
    type_valid = entry[1] in ['INF', 'SHM', 'MHM', 'CAA', 'OPM', 'AEM']
    focus_area_valid = bool(entry[2].strip())
    risk_level_valid = entry[3] in ['Low', 'Medium', 'High']
    tier_valid = entry[4] in ['1', '2', '3']
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
        return focus_area.strip(), "Tier " + tier.strip(), risk_level.strip()
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
                entry_data.append(validate_entry(entry_data))  # Check validity
                parsed_data.append(entry_data)
            else:
                if entry.strip():  # Ensure we don't log empty entries
                    with open('failed_to_parse.txt', 'a') as f:
                        f.write(f"Failed to parse ENTRY {record_id} | {current_type}: {entry}\n")

    return pd.DataFrame(parsed_data, columns=['Record ID', 'Type', 'Focus Area', 'Risk Level', 'Tier', 'Valid'])

# Read CSV with pandas
dataset = pd.read_csv('input.csv')
parsed_data = pd.concat([parse_comment(row['Record ID'], row['SMART Record Comment']) for _, row in dataset.iterrows()])
parsed_data.to_csv('_parsed_pandas_output.csv', index=False)
print("Parsing complete.")