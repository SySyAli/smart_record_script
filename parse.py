import csv
import re

input_file = "output.csv"
output_file = "parsed_output.csv"

# Validation function to check the integrity of each entry
def validate_entry(entry):
    type_valid = entry[0] in ['INF', 'SHM', 'MHM', 'CAA', 'OPM', 'AEM']
    focus_area_valid = bool(entry[1])  # Checks if there's a non-empty focus area
    risk_level_valid = entry[2] in ['Low', 'Medium', 'High', '']  # Empty is allowed if no risk level is mentioned
    tier_valid = entry[3] in ['Tier 1', 'Tier 2', 'Tier 3', '']  # Empty is allowed if no tier is mentioned
    return type_valid and focus_area_valid and risk_level_valid and tier_valid

# Parsing function using specific text markers
def parse_comment(comment):
    parsed_data = []
    # Regex pattern that extracts each type section with its content
    pattern = r"SMART \((INF|SHM|MHM|CAA|OPM|AEM)\): (.*?)(?=\s*SMART \((INF|SHM|MHM|CAA|OPM|AEM)\)|$)"
    matches = re.findall(pattern, comment, re.DOTALL)
    
    for match in matches:
        current_type = match[0]
        content = match[1]
        # Further extraction based on known structure within each type
        focus_areas = re.findall(r"([^\(\)\-–]+)(?: – |-)? (?:Tier ([1-3]) )?\(Risk Level (Low|Medium|High)\)?", content)
        
        for fa in focus_areas:
            focus_area, tier, risk_level = fa
            # Collect each entry
            entry_data = [current_type, focus_area.strip(), risk_level.strip(), tier.strip()]
            # Validate and flag the entry
            is_valid = 'Yes' if validate_entry(entry_data) else 'No'
            entry_data.append(is_valid)
            parsed_data.append(entry_data)
    
    return parsed_data

# Reading and writing CSV
with open(input_file, mode='r', newline='', encoding='utf-8') as file, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(file)
    writer = csv.writer(outfile)
    # Writing header for the new CSV
    writer.writerow(['Type', 'Focus Area', 'Risk Level', 'Tier', 'Valid'])
    print("Parsing CSV data...")
    for row in reader:
        print(f"Parsing comment: {row}")
        comment = row[0]  # Assuming the comment is in the first column
        parsed_comments = parse_comment(comment)
        for data in parsed_comments:
            writer.writerow(data)

print("CSV parsing complete and new file created with validity flag.")
