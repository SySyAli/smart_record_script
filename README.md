# SMART Comment Generation and Parsing Tool

This repository contains two Python scripts:
1. `generate.py` - Generates simulated SMART record comments and outputs them to a CSV file.
2. `parse.py` - Parses the generated comments to extract specific data and validate their format, saving the results to a separate CSV file and logging any parse failures to a text file.

## Setup

### Prerequisites

- Python 3.x

### Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/SySyAli/smart_record_script.git
cd smart_record_script
```

## Usage
### generate.py
To generate the data, run the `generate.py` script. This script will create a file named `output.csv` containing randomly generated SMART record comments.

- Function types (INF, SHM, MHM, CAA, OPM, AEM)
- Focus areas (e.g., "Focus Area 1")
- Risk levels (e.g., "Low", "Medium", "High")
- Tiers (only for certain types like SHM and MHM)
The entries are formatted into a simulated SMART comment and written to a CSV file.

### parse.py
The `parse.py` script reads the generated CSV, applies regex operations to extract information based on predefined patterns, and checks if the extracted data meet the validation criteria:

- Record ID is present
- Type is one of the predefined types (e.g., INF, SHM)
- Focus area and risk level are appropriately labeled
- Tier information is present when required (SHM and MHM)

Valid entries are saved to `parsed_output.csv`, and any errors encountered during parsing are logged to `failed_to_parse.txt`.

## Contributing
Feel free to fork this repository and submit pull requests or create issues for any improvements or bug fixes.

