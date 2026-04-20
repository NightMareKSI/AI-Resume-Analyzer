from skills_database import get_all_skills
import re


def extract_skills(text):

    if not text:
        return []

    text = text.lower()

    skills = get_all_skills()

    found_skills = set()

    for skill in skills:

        skill_lower = skill.lower()

        # Escape special regex characters
        escaped_skill = re.escape(skill_lower)

        # Allow spaces or slashes between words
        pattern = r'(?<!\w)' + escaped_skill + r'(?!\w)'

        if re.search(pattern, text):

            found_skills.add(skill_lower)

    return list(found_skills)


# Test block
if __name__ == "__main__":

    sample_text = """
    I have experience in Python, SQL, Machine Learning and Docker.
    """

    detected_skills = extract_skills(sample_text)

    print("Detected Skills:")
    print(detected_skills)