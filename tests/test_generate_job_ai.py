# tests/test_generate_job_ai.py
import pytest
from playwright.sync_api import expect
import re
from pages.dashboard_page import DashboardPage

def test_generate_job_ai(multi_user_contexts):
    # Get a logged-in page for RECRUITER
    page = multi_user_contexts["RECRUITER"]["page"]

    dashboard_page = DashboardPage(page)
    assert dashboard_page.is_dashboard_loaded(), "❌ Dashboard not loaded after login"

    # Step 2: Click 'Post New Job'
    dashboard_page.click_post_new_job()

    # Step 1: Generate with AI
    page.get_by_role("button", name="Generate with AI").click()

    # Step 2: Add company
    page.locator("input[placeholder='Search here']").fill("Tailorbird")
    page.get_by_text("Add Company").click()
    expect(page.get_by_role("heading", name="Add Company Details")).to_be_visible(timeout=20000)

    page.get_by_role("textbox", name="Enter company name").fill("Tailorbird")
    page.get_by_role("textbox", name="Enter company URL").fill("Tailorbird.com")
    page.get_by_role("button", name="Save", exact=True).click()

    expect(page.get_by_role("heading", name=re.compile("Tailorbird", re.IGNORECASE))).to_be_visible(timeout=60000)

    # Step 3: Edit location
    page.locator("#field-city").get_by_title("Edit").click()
    page.locator("#field-city").get_by_role("textbox").fill("Tirupati")
    page.get_by_role("button", name="Update").click()
    expect(page.get_by_text("Tirupati", exact=True)).to_be_visible()

    # Step 4: Close modal
    page.locator("#custom-modal button >> nth=0").click()

    # Step 5: Search template
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
    expect(page.get_by_text("India", exact=True)).to_be_visible()
    expect(page.get_by_text(re.compile("Experience.*2.*5", re.IGNORECASE))).to_be_visible()
