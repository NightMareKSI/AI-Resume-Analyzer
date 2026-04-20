from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_description):
    documents = [resume_text, job_description]
    vectorizer = CountVectorizer()
    matrix = vectorizer.fit_transform(documents)
    similarity = cosine_similarity(matrix)
    score = similarity[0][1]
    return round(score * 100, 2)

def find_missing_skills(resume_skills, jd_skills):
    missing = list(set(jd_skills) - set(resume_skills))
    return missing

if __name__ == "__main__":
    resume_text = "Python SQL React MongoDB"
    job_description = "Python SQL AWS Docker"
    score = calculate_similarity(resume_text, job_description)
    print("Match Score:", score, "%")