import json
import re

INPUT_FILE = "skills.json"
OUTPUT_FILE = "skills_fixed.json"

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

fixed_data = {}

for skill, info in data.items():

    # Remove _number suffix
    clean_skill = re.sub(r'_\d+$', '', skill)

    fixed_data[clean_skill] = info

with open(OUTPUT_FILE, "w") as f:
    json.dump(fixed_data, f, indent=2)

print("Skills fixed successfully")
print("Total skills:", len(fixed_data))