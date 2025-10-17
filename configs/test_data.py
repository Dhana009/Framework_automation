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
    "position": "Software Test Engineer testing",
    "internal_title": "testing",
    "headcount": 1,
    "job_type": "Test",
    "department": "QA",
    "location1": "India",
    "currency": "₹",
    "salary_min": 200001,
    "salary_max": 400002,
    "salary_duration": "Per day",
    "salary_note": "testing salary note",
}
