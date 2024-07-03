# For PowerBI use
import pandas as pd
import re

vessel_types = ["Barge", "Bulk Carrier", "Chemical Carrier", "Container Carrier", 
                "Dredge", "Fishing Vessel", "Ferry", "Oil Carrier", "Towboat", "Tug", "Yacht"]
function_types = ["INF", "SHM", "MHM", "CAA", "OPM", "AEM"]
focus_areas = ["Focus Area 1", "Focus Area 2", "Focus Area 3", "Focus Area 4"]
risk_levels = ["Low", "Medium", "High"]
tiers = ["Tier 1", "Tier 2", "Tier 3"]

def validate_entry(entry):
    id_valid = entry[0] is not None
    vessel_type_valid = entry[1] in vessel_types
    type_valid = entry[2] in function_types
    focus_area_valid = bool(entry[3].strip())
    risk_level_valid = entry[4] in risk_levels
    tier_valid = entry[5] in tiers
    if entry[2] in ['SHM', 'MHM']:
        return id_valid and vessel_type_valid and type_valid and focus_area_valid and risk_level_valid and tier_valid
    else:
        return id_valid and vessel_type_valid and type_valid and focus_area_valid and risk_level_valid

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

def parse_comment(record_id, vessel_type, comment):
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
                entry_data = [record_id, vessel_type, current_type, focus_area, risk_level, tier]
                entry_data.append(validate_entry(entry_data))  # Check validity
                parsed_data.append(entry_data)
            else:
                if entry.strip():  # Ensure we don't log empty entries
                    with open('failed_to_parse.txt', 'a') as f:
                        f.write(f"Failed to parse ENTRY {record_id} ({vessel_type})| {current_type}: {entry}\n")

    return pd.DataFrame(parsed_data, columns=['Record ID', 'Vessel Type','Type', 'Focus Area', 'Risk Level', 'Tier', 'Valid'])

# Read CSV with pandas
parsed_data = pd.concat([parse_comment(row['Record ID'], row['Vessel Type'],row['SMART Record Comment']) for _, row in dataset.iterrows()])