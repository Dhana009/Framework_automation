import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.job_details_page import JobDetailsPage
from configs.config import BASE_URL, USERS
from configs.test_data import JOB_FILE_PATH, JOB_DETAILS
from configs.constants import SUCCESS_MESSAGE_JOB_CREATED


@pytest.mark.regression
def test_create_new_job(page):
    # Step 0: Login (get credentials from config)
    login_page = LoginPage(page)
    login_page.open_login_page(BASE_URL)
    login_page.login(USERS["first_login"]["username"], USERS["first_login"]["password"])

    # Step 1: Dashboard
    dashboard_page = DashboardPage(page)
    assert dashboard_page.is_dashboard_loaded(), "❌ Dashboard not loaded after login"

    # Step 2: Click 'Post New Job'
    dashboard_page.click_post_new_job()

    # Step 3: Job Details workflow
    job_page = JobDetailsPage(page)
    job_page.upload_document(JOB_FILE_PATH)
    job_page.trigger_parsing()
    job_page.wait_for_parsed_state()

    job_page.verify_autofilled_fields(
        job_title=JOB_DETAILS["job_title"],
        company_name=JOB_DETAILS["company_name"],
        location=JOB_DETAILS["location"]
    )

    job_page.publish_job()
    job_page.verify_success_modal(SUCCESS_MESSAGE_JOB_CREATED)
    job_page.click_view_job()

    # Now use new extended functions
    job_page.open_edit_mode()
    job_page.fill_basic_job_details("Software Test Engineer testing", "testing", 1)
    job_page.add_job_type_and_department("Test", "QA")
    job_page.select_location("India")
    job_page.fill_salary_details(200001, 400002, "₹", "Per day", "salary testing")
    job_page.preview_job()
    job_page.publish_updated_job()
    job_page.view_published_job()

    job_page.open_edit_mode()
    job_page.fill_basic_job_details(
        JOB_DETAILS["position"],
        JOB_DETAILS["internal_title"],
        JOB_DETAILS["headcount"]
    )
    job_page.add_job_type_and_department(
        JOB_DETAILS["job_type"],
        JOB_DETAILS["department"]
    )
    job_page.select_location(JOB_DETAILS["location1"])
    job_page.fill_salary_details(
        JOB_DETAILS["salary_min"],
        JOB_DETAILS["salary_max"],
        JOB_DETAILS["currency"],
        JOB_DETAILS["salary_duration"],
        JOB_DETAILS["salary_note"]
    )
    job_page.preview_job()
    job_page.publish_updated_job()
    job_page.view_published_job()

