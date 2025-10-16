# tests/test_create_job.py

import pytest
from pages.dashboard_page import DashboardPage
from pages.job_details_page import JobDetailsPage
from configs.test_data import JOB_FILE_PATH, JOB_DETAILS
from configs.constants import SUCCESS_MESSAGE_JOB_CREATED


@pytest.mark.regression
def test_create_new_job(multi_user_contexts):
    # Use the RECRUITER user for this test
    page = multi_user_contexts["RECRUITER"]["page"]

    # Step 1: Dashboard
    dashboard_page = DashboardPage(page)
    assert dashboard_page.is_dashboard_loaded(), "❌ Dashboard not loaded after login"

    # Step 2: Click 'Post New Job'
    dashboard_page.click_post_new_job()

    # Step 3: Job Details workflow
    job_page = JobDetailsPage(page)

    # Upload and parse document
    job_page.upload_document(JOB_FILE_PATH)
    job_page.trigger_parsing()
    job_page.wait_for_parsed_state()  # ensure parse completed before validation

    # Verify parsed autofill details
    job_page.verify_autofilled_fields(
        job_title=JOB_DETAILS["job_title"],
        company_name=JOB_DETAILS["company_name"],
        location=JOB_DETAILS["location"]
    )

    # Publish the job
    job_page.publish_job()
    job_page.verify_success_modal(SUCCESS_MESSAGE_JOB_CREATED)

    # View Job and verify navigation
    job_page.click_view_job()
