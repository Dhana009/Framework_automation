# configs/test_data.py
import os

# Base data directory
DATA_DIR = os.path.join(os.getcwd(), "data")

# File paths
JOB_FILE_PATH = os.path.join(DATA_DIR, "sample_jobs", "Software_Test_Engineer.pdf")

JOB_DETAILS = {
    "job_title": "Software Test",
    "company_name": "SproutsAI",
    "location": "Hyderabad",
}
