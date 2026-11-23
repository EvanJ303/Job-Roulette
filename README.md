# Job Roulette

Job-matching database for ProfHacks 2025.

## Overview

Job Roulette is a Python desktop application for matching a resume to a catalog of job listings. It provides two main workflows through a Tkinter interface:

- **Search for jobs:** Paste a resume, set an optional minimum cosine-similarity score, and spin a roulette-style wheel to randomly select a qualifying job.
- **Post a job:** Enter a job title and description to add or update it in a MongoDB database.

The search flow loads all job listings from MongoDB, creates SBERT embeddings for the resume and job descriptions, ranks them by cosine similarity, and filters out scores below the chosen threshold. One of the remaining jobs is selected randomly and displayed with a generated analysis of how the resume matches that position. This analysis is produced by a Hugging Face Flan-T5 text-generation pipeline.

## How It Works

- `src/app/main.py` launches the main Tkinter menu and opens the search or posting window.
- `src/gui/search_interface.py` accepts the resume and minimum score, performs the roulette selection, and displays the winning job and AI analysis.
- `src/gui/post_interface.py` provides the form for adding or updating a job listing.
- `src/backend/db_to_dict.py` and `src/backend/dict_to_db.py` read and write job titles and descriptions in MongoDB.
- `src/backend/search.py` pairs each job title with its computed match score.
- `src/backend/match.py` uses `paraphrase-MiniLM-L6-v2` and cosine similarity to rank jobs.
- `src/backend/analyze.py` uses `google/flan-t5-large` to explain the strengths and weaknesses of a resume for a selected job.

The application expects MongoDB to run locally and uses:

- URI: `mongodb://localhost:27017/`
- Database: `job_database`
- Collection: `jobs`

Job documents are stored with `title` and `description` fields.

## Requirements

- Python 3
- A graphical desktop environment supported by Tkinter
- A running local MongoDB server
- Internet access on the first run to download the Hugging Face and Sentence Transformers models
- The following Python packages:

```text
pymongo
sentence-transformers
scikit-learn
transformers
torch
```

Tkinter is normally included with standard Python installations on many platforms, but may need to be installed separately through your operating system package manager.

## Usage

### 1. Start MongoDB

Start MongoDB locally on port `27017`. The application expects to connect to the database `job_database` and collection `jobs` automatically.

For example, with MongoDB running as a local service:

```bash
mongosh
```

The database and collection are created when the application first inserts a job.

### 2. Clone the repository and install dependencies

Run these commands from the repository root:

```bash
git clone https://github.com/EvanJ303/Job-Roulette.git
cd Job-Roulette
python3 -m pip install pymongo sentence-transformers scikit-learn transformers torch
```

On systems where Python is launched as `python` instead of `python3`, replace `python3` in the commands below with `python`.

### 3. Launch the application

From the repository root:

```bash
python3 src/app/main.py
```

This opens the Job Roulette menu.

### Search for a job

1. Select **Search for Jobs**.
2. Paste your resume into the resume text area.
3. Enter a minimum match score, such as `0.2`, or leave it empty to accept all scores.
4. Click **Spin the Wheel**.
5. Confirm the randomly selected job from the wheel window.
6. Review the job title, description, cosine-similarity score, and generated resume analysis.

Match scores range from approximately `-1` to `1`. Higher scores indicate greater semantic similarity between the resume and job description. The roulette choice is random only among jobs that meet the configured minimum score.

### Post a job

1. Select **Post a Job**.
2. Enter a job title and description.
3. Click **Post Job**.

If the title already exists, its description is updated. Otherwise, a new document is inserted into MongoDB.

## Running Backend Modules Directly

The backend modules can also be exercised independently. For example, to run the sample resume and job analysis:

```bash
python3 src/backend/analyze.py
```

Run commands from the repository root because the GUI and backend modules use repository-relative paths.
