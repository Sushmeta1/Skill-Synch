import docx2txt
import PyPDF2
import os
import re

# Cleaned skill list
SKILL_DB = {
    "technical": [
        "Python", "Java", "Node.js", "React", "Flask", "Django", "Docker",
        "Kubernetes", "AWS", "GCP", "Azure", "MySQL", "PostgreSQL", "MongoDB",
        "HTML", "CSS", "JavaScript", "TypeScript", "Git", "REST API", "SQL",
        "CI/CD", "Linux", "Firebase", "Redis", "GraphQL", "NoSQL"
    ],
    "soft": [
        "Communication", "Teamwork", "Leadership", "Problem Solving",
        "Critical Thinking", "Time Management", "Adaptability", "Collaboration"
    ]
}

# Common non-skill words to ignore
STOPWORDS = {
    "experience", "knowledge", "skills", "strong", "with", "and", "or",
    "of", "the", "a", "an", "in", "on", "for", "to", "hands-on", "good", "excellent", "familiarity", "understanding"
}

def extract_text_from_file(file_path):
    text = ""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        with open(file_path, "rb") as f:
            pdf = PyPDF2.PdfReader(f)
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
    elif ext in [".docx", ".doc"]:
        text = docx2txt.process(file_path)
    else:
        raise ValueError("Unsupported file format")
    return text.lower()

def clean_text(text):
    return re.sub(r"[^a-zA-Z0-9+.# ]", " ", text).lower()

def extract_skills(text, skill_list):
    matched = []
    for skill in skill_list:
        skill_clean = skill.lower()
        if skill_clean in STOPWORDS:
            continue
        pattern = r"\b" + re.escape(skill_clean) + r"\b"
        if re.search(pattern, text):
            matched.append(skill)
    return matched

def match_resume_to_job(resume_path, job_description):
    resume_text = clean_text(extract_text_from_file(resume_path))
    job_text = clean_text(job_description)

    all_skills = SKILL_DB["technical"] + SKILL_DB["soft"]

    resume_skills = extract_skills(resume_text, all_skills)
    job_skills = extract_skills(job_text, all_skills)

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    score = int((len(matched) / max(len(job_skills), 1)) * 100)

    suggestions = [f"Consider adding more experience with {s}" for s in missing]

    return {
        "similarity_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "improvement_areas": suggestions,
        "skill_categories": {
            "Technical": [s for s in resume_skills if s in SKILL_DB["technical"]],
            "Soft Skills": [s for s in resume_skills if s in SKILL_DB["soft"]],
            "Missing Technical": [s for s in missing if s in SKILL_DB["technical"]],
            "Missing Soft Skills": [s for s in missing if s in SKILL_DB["soft"]],
        }
    }
