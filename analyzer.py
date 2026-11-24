
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ml.skills import extract_skills


def analyze_resume(resume_text, job_description):

    # Extract skills
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    # Identify matching and missing skills
    matched_skills = [
        skill for skill in job_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill for skill in job_skills
        if skill not in resume_skills
    ]

    # Calculate TF-IDF similarity
    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    match_score = round(float(similarity) * 100, 2)

    # Generate suggestions
    suggestions = []

    if missing_skills:
        suggestions.append(
            "Consider learning these required skills: "
            + ", ".join(missing_skills)
        )

    if match_score < 40:
        suggestions.append(
            "Customize your resume to better match the job description."
        )

    if not matched_skills:
        suggestions.append(
            "Add relevant technical skills and projects to your resume."
        )

    if not suggestions:
        suggestions.append(
            "Your resume looks relevant. Keep improving your project descriptions."
        )

    return {
        "match_score": match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions
    }
