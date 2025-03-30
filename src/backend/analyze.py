from transformers import pipeline

analysis_pipeline = pipeline("text2text-generation", model="google/flan-t5-large")

def analyse_job(resume, job_description):
    """
    Analyzes the relationship between a resume and a job description using Flan-T5.
    """
    prompt = (
        f"Analyze the following resume and job description to determine how well they match. "
        f"Provide a detailed explanation of the strengths and weaknesses of the resume in relation "
        f"to the job description. Be specific about which skills and experiences align or do not align.\n\n"
        f"Resume:\n{resume}\n\n"
        f"Job Description:\n{job_description}\n\n"
        f"Provide a detailed analysis:"
    )

    response = analysis_pipeline(prompt, max_length=300, num_return_sequences=1)
    return response[0]["generated_text"]

if __name__ == "__main__":
    resume = (
        "Data scientist with 5 years of experience in Python programming, machine learning, "
        "and data visualization. Skilled in building predictive models, analyzing large datasets, "
        "and creating insightful visualizations to support business decisions. Proficient in tools "
        "like TensorFlow, Pandas, and Matplotlib. Experienced in working with cross-functional teams "
        "to deliver data-driven solutions."
    )
    job_description = (
        "We are seeking a data scientist with strong Python skills, experience in "
        "machine learning, and the ability to create data visualizations. The ideal "
        "candidate should have experience working with large datasets and building predictive models."
    )

    result = analyse_job(resume, job_description)
    print("Analysis Result:")
    print(result)