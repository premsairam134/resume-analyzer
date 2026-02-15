import pandas as pd


def recommend_jobs(extracted_skills):
    """
    Recommends top job roles based on extracted skills.
    Returns: List of dicts with job role, matching skills, and missing skills.
    """
    try:
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        dataset_path = os.path.join(base_dir, 'dataset', 'jobs.csv')
        df = pd.read_csv(dataset_path)
    except Exception as e:
        print(f"Error reading dataset: {e}")
        return []

    if not extracted_skills:
        return []

    # Prepare data for simple matching
    jobs = []
    
    # Simple set matching approach for interpretability and speed
    extracted_set = set([skill.lower() for skill in extracted_skills])

    for index, row in df.iterrows():
        job_role = row['Job Role']
        
        # Split skills from CSV string
        required_skills = [s.strip().lower() for s in str(row['Skills']).split(',')]
        required_set = set(required_skills)
        
        match_count = 0
        missing = []
        matching = []
        
        for skill in required_set:
            if skill in extracted_set:
                match_count += 1
                matching.append(skill.title())
            else:
                missing.append(skill.title())
        
        score = (match_count / len(required_set)) * 100 if required_set else 0

        jobs.append({
            'role': job_role,
            'match_score': round(score, 2),
            'matching_skills': matching,
            'missing_skills': missing
        })

    # Sort by match score descending
    jobs.sort(key=lambda x: x['match_score'], reverse=True)
    
    return jobs[:5]
