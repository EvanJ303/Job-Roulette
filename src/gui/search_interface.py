import tkinter as tk
from tkinter import ttk, messagebox
import random
import sys
import time

# Explicitly specify the path to the backend modules
sys.path.append("./src/backend")
from db_to_dict import fetch_jobs_from_db
from search import compute_job_title_scores
from analyze import analyse_job  # Import the analyse_job function

def fetch_and_display_jobs(uri, db_name, collection_name, resume, min_score):
    """
    Fetches jobs from the database, computes match scores, and displays them in the table.

    Args:
        uri (str): MongoDB connection URI.
        db_name (str): Database name.
        collection_name (str): Collection name.
        resume (str): The resume text.
        min_score (float): Minimum match score for filtering jobs.

    Returns:
        None
    """
    try:
        # Fetch jobs from the database
        job_data = fetch_jobs_from_db(uri, db_name, collection_name)

        # Compute match scores
        job_scores = compute_job_title_scores(resume, job_data)

        # Sort jobs by match score in descending order
        sorted_job_scores = sorted(job_scores.items(), key=lambda x: x[1], reverse=True)

        # Filter jobs that meet the minimum score
        filtered_jobs = [(job_title, score) for job_title, score in sorted_job_scores if score >= min_score]

        if not filtered_jobs:
            messagebox.showinfo("No Jobs Found", "No jobs match the criteria. Try again!")
            return

        # Simulate a roulette spin
        spin_result = random.choice(filtered_jobs)

        # Perform analysis of the winning job and resume
        analysis_result = analyse_job(resume, job_data[spin_result[0]])

        # Display the winning job and analysis in a pop-up window
        show_winning_job(spin_result[0], job_data[spin_result[0]], spin_result[1], analysis_result)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def show_spinning_wheel(filtered_jobs, callback):
    """
    Displays a spinning wheel animation and selects a random job.

    Args:
        filtered_jobs (list): List of filtered jobs with their scores.
        callback (function): Function to call with the selected job.

    Returns:
        None
    """
    # Create a spinning wheel window
    wheel_window = tk.Toplevel(root)
    wheel_window.title("Spinning Wheel 🎡")
    wheel_window.geometry("400x400")
    wheel_window.configure(bg="#222222")

    # Create a canvas for the spinning wheel
    canvas = tk.Canvas(wheel_window, width=300, height=300, bg="#222222", highlightthickness=0)
    canvas.pack(pady=20)

    # Add spinning text
    text_id = canvas.create_text(150, 150, text="", fill="#FFD700", font=("Arial", 16, "bold"))

    # Simulate spinning
    for _ in range(30):  # Number of spins
        random_job = random.choice(filtered_jobs)
        canvas.itemconfig(text_id, text=random_job[0])  # Update the text with a random job title
        wheel_window.update()
        time.sleep(0.1)  # Pause to simulate spinning

    # Select the final job
    selected_job = random.choice(filtered_jobs)
    canvas.itemconfig(text_id, text=f"🎉 {selected_job[0]} 🎉")  # Highlight the final job

    # Add a button to confirm the selection
    tk.Button(
        wheel_window,
        text="Confirm",
        bg="#FFD700",
        fg="#222222",
        font=("Arial", 12, "bold"),
        command=lambda: [callback(selected_job), wheel_window.destroy()],
    ).pack(pady=20)

def show_winning_job(job_title, job_description, score, analysis_result):
    """
    Displays the winning job and its analysis in a new window.

    Args:
        job_title (str): The title of the winning job.
        job_description (str): The description of the winning job.
        score (float): The match score of the winning job.
        analysis_result (str): The analysis result of the resume and job description.

    Returns:
        None
    """
    # Create a new window to display the winning job
    winning_window = tk.Toplevel(root)
    winning_window.title("🎰 Winning Job!")
    winning_window.geometry("600x500")
    winning_window.configure(bg="#222222")

    # Display the job title
    tk.Label(
        winning_window,
        text=f"🎉 {job_title} 🎉",
        bg="#222222",
        fg="#FFD700",
        font=("Arial", 20, "bold"),
    ).pack(pady=10)

    # Display the match score
    tk.Label(
        winning_window,
        text=f"Match Score: {score:.2f}",
        bg="#222222",
        fg="#FFFFFF",
        font=("Arial", 14),
    ).pack(pady=5)

    # Display the job description
    description_label = tk.Label(
        winning_window,
        text="Job Description:",
        bg="#222222",
        fg="#FFFFFF",
        font=("Arial", 12, "bold"),
    )
    description_label.pack(pady=5)
    description_text = tk.Text(winning_window, wrap="word", font=("Arial", 12), bg="#333333", fg="#FFFFFF", height=8)
    description_text.insert("1.0", job_description)
    description_text.configure(state="disabled")  # Make the text read-only
    description_text.pack(fill="both", expand=False, padx=10, pady=5)

    # Display the analysis result
    analysis_label = tk.Label(
        winning_window,
        text="Analysis Result:",
        bg="#222222",
        fg="#FFFFFF",
        font=("Arial", 12, "bold"),
    )
    analysis_label.pack(pady=5)
    analysis_text = tk.Text(winning_window, wrap="word", font=("Arial", 12), bg="#333333", fg="#FFFFFF", height=8)
    analysis_text.insert("1.0", analysis_result)
    analysis_text.configure(state="disabled")  # Make the text read-only
    analysis_text.pack(fill="both", expand=False, padx=10, pady=5)

def spin_roulette():
    """
    Simulates spinning the roulette wheel to filter jobs.
    """
    resume = resume_text.get("1.0", tk.END).strip()
    min_score = float(min_score_entry.get()) if min_score_entry.get() else 0.0

    def callback(selected_job):
        job_title, score = selected_job
        job_description = fetch_jobs_from_db(uri, db_name, collection_name)[job_title]
        analysis_result = analyse_job(resume, job_description)
        show_winning_job(job_title, job_description, score, analysis_result)

    try:
        # Fetch jobs from the database
        job_data = fetch_jobs_from_db(uri, db_name, collection_name)

        # Compute match scores
        job_scores = compute_job_title_scores(resume, job_data)

        # Sort jobs by match score in descending order
        sorted_job_scores = sorted(job_scores.items(), key=lambda x: x[1], reverse=True)

        # Filter jobs that meet the minimum score
        filtered_jobs = [(job_title, score) for job_title, score in sorted_job_scores if score >= min_score]

        if not filtered_jobs:
            messagebox.showinfo("No Jobs Found", "No jobs match the criteria. Try again!")
            return

        # Show the spinning wheel
        show_spinning_wheel(filtered_jobs, callback)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Initialize the main application window
root = tk.Tk()
root.title("Job Matcher Casino 🎰")
root.geometry("900x600")
root.configure(bg="#222222")

# Header
header_frame = tk.Frame(root, bg="#FFD700", height=50)
header_frame.pack(fill="x")
header_label = tk.Label(
    header_frame,
    text="Job Matcher Casino 🎰",
    bg="#FFD700",
    fg="#222222",
    font=("Arial", 24, "bold"),
)
header_label.pack(pady=10)

# Main content frame
content_frame = tk.Frame(root, bg="#222222", padx=20, pady=20)
content_frame.pack(fill="both", expand=True)

# Resume input
tk.Label(content_frame, text="Resume:", bg="#222222", fg="#FFFFFF", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
resume_text = tk.Text(content_frame, height=5, width=60, font=("Arial", 10), bg="#333333", fg="#FFFFFF")
resume_text.grid(row=1, column=0, columnspan=2, pady=5)

# Minimum match score input
tk.Label(content_frame, text="Minimum Match Score:", bg="#222222", fg="#FFFFFF", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
min_score_entry = tk.Entry(content_frame, font=("Arial", 10), width=10, bg="#333333", fg="#FFFFFF")
min_score_entry.grid(row=2, column=1, sticky="w", pady=5)

# Spin button
spin_button = tk.Button(
    content_frame,
    text="🎰 Spin the Wheel!",
    bg="#FFD700",
    fg="#222222",
    font=("Arial", 14, "bold"),
    padx=10,
    pady=5,
    command=spin_roulette,
)
spin_button.grid(row=3, column=0, columnspan=2, pady=20)

# MongoDB connection details
uri = "mongodb://localhost:27017/"
db_name = "job_database"
collection_name = "jobs"

# Run the application
root.mainloop()