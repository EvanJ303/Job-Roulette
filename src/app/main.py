import tkinter as tk
import subprocess
import sys

def open_search_interface():
    """
    Opens the search interface by running the search_interface.py script.
    """
    subprocess.Popen([sys.executable, "./src/gui/search_interface.py"])

def open_post_interface():
    """
    Opens the post interface by running the post_interface.py script.
    """
    subprocess.Popen([sys.executable, "./src/gui/post_interface.py"])

# Initialize the main application window
root = tk.Tk()
root.title("Job Roulette")
root.geometry("400x300")
root.configure(bg="#222222")

# Header
header_frame = tk.Frame(root, bg="#FFD700", height=50)
header_frame.pack(fill="x")
header_label = tk.Label(
    header_frame,
    text="Job Roulette",
    bg="#FFD700",
    fg="#222222",
    font=("Arial", 24, "bold"),
)
header_label.pack(pady=10)

# Main content frame
content_frame = tk.Frame(root, bg="#222222", padx=20, pady=20)
content_frame.pack(fill="both", expand=True)

# Instruction label
instruction_label = tk.Label(
    content_frame,
    text="What would you like to do?",
    bg="#222222",
    fg="#FFFFFF",
    font=("Arial", 14),
)
instruction_label.pack(pady=20)

# Button to open the search interface
search_button = tk.Button(
    content_frame,
    text="Search for Jobs",
    bg="#4CAF50",
    fg="white",
    font=("Arial", 14, "bold"),
    padx=10,
    pady=5,
    command=open_search_interface,
)
search_button.pack(pady=10)

# Button to open the post interface
post_button = tk.Button(
    content_frame,
    text="Post a Job",
    bg="#2196F3",
    fg="white",
    font=("Arial", 14, "bold"),
    padx=10,
    pady=5,
    command=open_post_interface,
)
post_button.pack(pady=10)

# Run the application
root.mainloop()