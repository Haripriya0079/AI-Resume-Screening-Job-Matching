
import re

# Skills database
SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "HTML",
    "CSS",
    "React",
    "Node.js",
    "Flask",
    "Django",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Data Science",
    "Data Analysis",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Excel",
    "Power BI",
    "Tableau",
    "Git",
    "GitHub",
    "Linux",
    "AWS",
    "Azure",
    "Docker",
    "Kubernetes",
    "REST API",
    "Communication",
    "Problem Solving",
    "Teamwork",
    "Leadership"
]


def extract_skills(text):
    found_skills = []

    text = text.lower()

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills
