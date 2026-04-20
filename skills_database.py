import json

# Load skills from JSON file
with open(
    "skills.json",
    "r",
    encoding="utf-8"
) as f:

    SKILLS_DATABASE = json.load(f)


def get_all_skills():
    return [s.lower().strip() for s in SKILLS_DATABASE.keys()]