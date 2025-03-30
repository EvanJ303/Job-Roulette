import sys

# Explicitly specify the path to the backend modules
sys.path.append("./src/backend")
from match import compute_match_scores

def compute_job_title_scores(resume, job_data):
    """
    Computes match scores between a resume and a dictionary of job titles with their descriptions.

    Args:
        resume (str): The resume text.
        job_data (dict): A dictionary where keys are job titles and values are job descriptions.

    Returns:
        dict: A dictionary where keys are job titles and values are match scores.
    """
    # Extract job titles and descriptions
    job_titles = list(job_data.keys())
    job_descriptions = list(job_data.values())

    # Compute match scores using the function from match.py
    match_scores = compute_match_scores(resume, job_descriptions)

    # Create a dictionary of job titles with their corresponding match scores
    job_title_scores = {job_titles[i]: match_scores[i] for i in range(len(job_titles))}

    return job_title_scores