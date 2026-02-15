def calculate_score(text, extracted_skills, recommended_jobs):
    """
    Calculates a resume score out of 100 based on various factors.
    Returns: Score (int), Feedback (list of strings).
    """
    score = 0
    feedback = []

    # 1. Skill Match Score (up to 40 points)
    # Based on match with the top recommended job
    if recommended_jobs:
        top_job = recommended_jobs[0]
        match_percentage = top_job['match_score']
        score += (match_percentage * 0.4) # 40% weight
        
        if match_percentage < 50:
            feedback.append("Low skill match for top recommended role. Consider learning required skills.")
    else:
        feedback.append("No clear job role match found based on skills.")

    # 2. Key Sections Check (up to 30 points)
    sections = {
        'Experience': ['experience', 'work history', 'employment', 'internships'],
        'Education': ['education', 'university', 'college', 'degree', 'gpa'],
        'Projects': ['projects', 'portfolio', 'GitHub'],
        'Skills': ['skills', 'technologies', 'proficiency']
    }
    
    text_lower = text.lower()
    
    for section, keywords in sections.items():
        if any(keyword in text_lower for keyword in keywords):
            score += 7.5  # 30 / 4 sections
        else:
            feedback.append(f"Missing '{section}' section. Add it to improve ATS parsing.")

    # 3. Resume Length & Formatting (up to 20 points)
    word_count = len(text.split())
    if 200 <= word_count <= 800:
        score += 20
    elif word_count < 200:
        score += 10
        feedback.append("Resume is too short. Add more details about your experience/projects.")
    else:
        score += 10
        feedback.append("Resume might be too long. Keep it concise (1-2 pages).")

    # 4. Measurable Results (up to 10 points)
    # Look for numbers/percentages which often indicate achievements
    import re
    metrics = re.findall(r'\d+%', text)
    if metrics:
        score += 10
    else:
        feedback.append("Add quantifiable results (e.g., 'Improved efficiency by 20%') to bullet points.")

    return min(100, round(score)), feedback
