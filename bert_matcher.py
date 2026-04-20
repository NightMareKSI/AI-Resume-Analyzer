from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_similarity(resume_text, job_description):
    resume_embedding = model.encode([resume_text])
    jd_embedding = model.encode([job_description])

    similarity = cosine_similarity(resume_embedding, jd_embedding)

    score = similarity[0][0]

    return round(score * 100, 2)

if __name__ == "__main__":

    resume_text = "Experienced Python developer with SQL and backend skills"

    job_description = "Looking for a Python engineer with database experience"

    score = calculate_semantic_similarity(
        resume_text,
        job_description
    )

    print("Semantic Match Score:", score, "%")