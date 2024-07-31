import csv
import re
import itertools
import pandas as pd

input_file = "input.csv"
output_file = "_parsed_output.csv"
combinations_file = "_combinations_output.csv"
failed_output_file = "failed_to_parse.txt"

vessel_types = ["Barge", "Bulk Carrier", "Chemical Carrier", "Container Carrier", 
                "Dredge", "Fishing Vessel", "Ferry", "Oil Carrier", "Towboat", "Tug", "Yacht"]
function_types = ["INF", "SHM", "MHM", "CAA", "OPM", "AEM"]
focus_areas = ["Focus Area 1", "Focus Area 2", "Focus Area 3", "Focus Area 4"]
risk_levels = ["Low", "Medium", "High"]
tiers = ["Tier 1", "Tier 2", "Tier 3"]

# clear the txt
open(failed_output_file, 'w').close()

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
        current_function = match[0]
        content = match[1]

        entries = re.split(r"\),?\s*", content.strip('.'))
        for entry in entries:
            if current_function in ['SHM', 'MHM']:
                focus_area, tier, risk_level = parse_shm_mhm(entry)
            else:
                focus_area, tier, risk_level = parse_general(entry)

            if focus_area and risk_level:
                entry_data = [record_id, vessel_type, current_function, focus_area, risk_level, tier]
                is_valid = 'True' if validate_entry(entry_data) else 'False'
                if is_valid == 'False':
                    print(f"FALSE Failed to parse ENTRY {record_id} ({vessel_type}) | {current_function}: {entry}")
                entry_data.append(is_valid)
                parsed_data.append(entry_data)
            else:
                if entry.strip():  # Ensure we do not log empty entries
                    with open(failed_output_file, 'a') as f:
                        f.write(f"Failed to parse ENTRY {record_id} ({vessel_type}) | {current_function}: {entry}\n")

    return parsed_data

def get_all_combinations(comment):
    # get all functions inside the comment and sort it alphabeticaly
    functions = sorted(set(re.findall(r"SMART \((INF|SHM|MHM|CAA|OPM|AEM)\)", comment)))
    # print(functions)
    #  generate all combinations of the functions array from length 2 to the length of the array and drop the duplicates and sort it and return it
    return sorted(set(itertools.chain.from_iterable(itertools.combinations(functions, r) for r in range(2, len(functions) + 1))))
    
    
# Reading and writing CSV
with open(input_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)

    data = []
    combinations_data = []
    next(reader)  # Skip header if present
    for row in reader:
        record_id = row[0]
        vessel_type = row[1]
        comment = row[2]
        parsed_comments = parse_comment(record_id, vessel_type, comment)
        all_combinations = get_all_combinations(comment)
        for parsed_data in parsed_comments:
            data.append(parsed_data)
        for combination in all_combinations:
            print(record_id, combination)
            combinations_data.append([record_id,  combination])

# Create a pandas DataFrame from the parsed data
df = pd.DataFrame(data, columns=['Record ID', 'Vessel Type', 'Function', 'Focus Area', 'Risk Level', 'Tier', 'Valid'])
df_comb = pd.DataFrame(combinations_data, columns=['Record ID', 'Function Combination'])

# Save the DataFrame to a CSV file
df.to_csv(output_file, index=False, encoding='utf-8')
df_comb.to_csv(combinations_file, index=False, encoding='utf-8')

print("CSV parsing complete. Output file created with data integrity checks.")

