def calculate_skill_match_score(resume_skills, jd_skills):

    if len(jd_skills) == 0:
        return 0
    
    matched_skills = set(resume_skills).intersection(set(jd_skills))

    score = (len(matched_skills) / len(jd_skills)) * 100

    return round(score, 2)

def calculate_overall_score(semantic_score, skill_score):
    semantic_weight = 0.6
    skill_weight = 0.4

    overall = (semantic_score * semantic_weight + skill_score * skill_weight)

    return round(overall, 2)