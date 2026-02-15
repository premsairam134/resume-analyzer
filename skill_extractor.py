import re
import spacy
from spacy.matcher import Matcher

try:
    nlp = spacy.load("en_core_web_sm")
except:
    # If model is not found, fallback to simpler processing or notify user
    nlp = spacy.blank("en")

def extract_skills(text):
    """
    Extracts skills from text using spaCy and a predefined skill list.
    """
    if not text:
        return []

    # Common technical skills list (can be expanded)
    skills_db = [
        "Python", "Java", "C++", "C#", "JavaScript", "HTML", "CSS", "SQL", "NoSQL",
        "React", "Angular", "Vue", "Node.js", "Django", "Flask", "Spring", "Hibernate",
        "Machine Learning", "Deep Learning", "NLP", "Data Analysis", "Data Science",
        "Power BI", "Tableau", "Excel", "Git", "GitHub", "Docker", "Kubernetes", "AWS",
        "Azure", "GCP", "Linux", "Unix", "Bash", "Shell Scripting", "Agile", "Scrum",
        "Project Management", "Communication", "Teamwork", "Problem Solving", "Leadership",
        "Time Management", "Critical Thinking", "Creativity", "Adaptability",
        "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas", "NumPy", "Matplotlib"
    ]

    found_skills = set()
    
    # Simple regex based search for robustness
    for skill in skills_db:
        # Create a regex pattern with word boundaries to match whole words/phrases
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text, re.IGNORECASE):
            found_skills.add(skill)

    # Use spaCy for more complex entities if needed (e.g. ORG, PRODUCT)
    doc = nlp(text)
    
    # Example: specific patterns could be used here
    # matcher = Matcher(nlp.vocab)
    # ...

    return list(found_skills)
