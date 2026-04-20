from skills_database import SKILLS_DATABASE


def get_skill_info(skill):

    # normalize skill name
    skill = skill.strip().lower()

    for db_skill in SKILLS_DATABASE:

        if db_skill.lower() == skill:

            return SKILLS_DATABASE[db_skill]

    return {
        "category": "Unknown",
        "description": "No description available",
        "demand_level": "Unknown"
    }