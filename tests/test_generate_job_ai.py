import pytest
from playwright.sync_api import expect
import re
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from configs.config import BASE_URL, USERS, EXPECT_TIMEOUT_job


@pytest.mark.regression
def test_generate_job_ai(page):
    # Step 0: Login (get credentials from config)
    login_page = LoginPage(page)
    login_page.open_login_page(BASE_URL)
    login_page.login(USERS["Second_login"]["username"], USERS["Second_login"]["password"])

    # Step 1: Dashboard
    dashboard_page = DashboardPage(page)
    assert dashboard_page.is_dashboard_loaded(), "❌ Dashboard not loaded after login"

    # Step 2: Click 'Post New Job'
    dashboard_page.click_post_new_job()

    # Step 3: Generate with AI
    page.get_by_role("button", name="Generate with AI").click()

    # ... rest of your flow remains unchanged ...


    # Step 4: Add company
    page.locator("input[placeholder='Search here']").fill("Tailorbird")
    page.get_by_text("Add Company").click()
    expect(page.get_by_role("heading", name="Add Company Details")).to_be_visible(timeout=20000)

    page.get_by_role("textbox", name="Enter company name").fill("Tailorbird")
    page.get_by_role("textbox", name="Enter company URL").fill("Tailorbird.com")
    page.get_by_role("button", name="Save", exact=True).click()
    expect(page.get_by_role("heading", name=re.compile("Tailorbird", re.IGNORECASE))).to_be_visible(timeout=60000)

    # Continue with rest of your steps...


    # Step 3: Edit location
    page.locator("#field-city").get_by_title("Edit").click()
    page.locator("#field-city").get_by_role("textbox").fill("Tirupati")
    page.get_by_role("button", name="Update").click()
    expect(page.get_by_text("Tirupati", exact=True)).to_be_visible()

    # Step 4: Close modal
    page.locator("#custom-modal button >> nth=0").click()

    # Step 5: Search template
    page.get_by_role("textbox", name="Search template").click()
    page.get_by_role("textbox", name="Search template").fill("software engineer")
    page.get_by_text("Fetch template for").click()

    # Step 6: Generate job
    page.get_by_role("textbox", name="Enter any additional").fill(
        "minimum 2 to 5 years of experience and India location"
    )
    page.get_by_role("button", name="Generate job").click()
    expect(page.get_by_text("Job generated")).to_be_visible(timeout=150000)

    # Step 7: Publish
    expect(page.get_by_role("button", name="Publish")).to_be_enabled()
    page.get_by_role("button", name="Publish").click()
    page.get_by_role("button", name="View Job").click()

    # Step 8: Verify
    expect(page.get_by_text("India", exact=True)).to_be_visible(timeout=EXPECT_TIMEOUT_job)
    expect(page.get_by_text(re.compile(r"Experience\s*2\s*[-–]\s*5\s*years", re.IGNORECASE)).first).to_be_visible()

