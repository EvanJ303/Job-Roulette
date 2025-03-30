from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize the SBERT model
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# Function to compute match scores for a given resume and job descriptions
def compute_match_scores(resume, job_descriptions):
    """
    Computes match scores between a resume and a list of job descriptions.

    Args:
        resume (str): The resume text.
        job_descriptions (list of str): A list of job description texts.

    Returns:
        list of float: A list of match scores (cosine similarity) for each job description.
    """
    # Encode the resume and job descriptions into embeddings
    resume_embedding = model.encode([resume], convert_to_tensor=False)[0]
    job_description_embeddings = model.encode(job_descriptions, convert_to_tensor=False)

    # Compute cosine similarity for each job description
    match_scores = [
        cosine_similarity([resume_embedding], [job_description_embedding])[0][0]
        for job_description_embedding in job_description_embeddings
    ]

    return match_scores