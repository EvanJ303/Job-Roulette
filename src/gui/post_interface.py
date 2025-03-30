import tkinter as tk
from tkinter import messagebox
import sys

# Explicitly specify the path to the backend modules
sys.path.append("./src/backend")
from dict_to_db import update_jobs_in_db

def post_job_to_db(uri, db_name, collection_name, job_title, job_description):
    """
    Posts a job title and description to the MongoDB database.

    Args:
        uri (str): MongoDB connection URI.
        db_name (str): Database name.
        collection_name (str): Collection name.
        job_title (str): The job title to post.
        job_description (str): The job description to post.

    Returns:
        None
    """
    try:
        # Create a dictionary with the job title and description
        jobs_dict = {job_title: job_description}

        # Update the database with the new job
        update_jobs_in_db(uri, db_name, collection_name, jobs_dict)

        # Show success message
        messagebox.showinfo("Success", f"Job '{job_title}' has been posted successfully!")

        # Clear the input fields
        job_title_entry.delete(0, tk.END)
        job_description_text.delete("1.0", tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Initialize the main application window
root = tk.Tk()
root.title("Post Job")
root.geometry("600x400")
root.configure(bg="#f4f4f4")

# Header
header_frame = tk.Frame(root, bg="#4CAF50", height=50)
header_frame.pack(fill="x")
header_label = tk.Label(
    header_frame,
    text="Post a Job",
    bg="#4CAF50",
    fg="white",
    font=("Arial", 18, "bold"),
)
header_label.pack(pady=10)

# Main content frame
content_frame = tk.Frame(root, bg="#f4f4f4", padx=20, pady=20)
content_frame.pack(fill="both", expand=True)

# Job title input
tk.Label(content_frame, text="Job Title:", bg="#f4f4f4", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
job_title_entry = tk.Entry(content_frame, width=40, font=("Arial", 10))
job_title_entry.grid(row=0, column=1, pady=5)

# Job description input
tk.Label(content_frame, text="Job Description:", bg="#f4f4f4", font=("Arial", 12)).grid(row=1, column=0, sticky="nw", pady=5)
job_description_text = tk.Text(content_frame, height=10, width=40, font=("Arial", 10), wrap="word")
job_description_text.grid(row=1, column=1, pady=5)

# Post button
post_button = tk.Button(
    content_frame,
    text="Post Job",
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=10,
    pady=5,
    command=lambda: post_job_to_db(
        uri,
        db_name,
        collection_name,
        job_title_entry.get().strip(),
        job_description_text.get("1.0", tk.END).strip(),
    ),
)
post_button.grid(row=2, column=0, columnspan=2, pady=10)

# MongoDB connection details
uri = "mongodb://localhost:27017/"
db_name = "job_database"
collection_name = "jobs"

# Run the application
root.mainloop()