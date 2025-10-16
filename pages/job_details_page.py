# pages/job_details_page.py

import time
from playwright.sync_api import Page, expect
from utils.logger import get_logger
from configs.test_data import JOB_FILE_PATH, JOB_DETAILS
from configs.constants import SUCCESS_MESSAGE_JOB_CREATED
import re

class JobDetailsPage:
    """Page Object for the 'Post New Job' (Job Details) section"""

    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

        # ---------- LOCATORS ----------

        # Buttons (Generate with AI / Upload / Autofill / Parsed)
        self.btn_generate_ai = "button:has-text('Generate with AI')"
        self.input_upload_file = "input#upload"
        self.drag_drop_zone = "div:has-text('Drag or click to browse')"
        self.btn_click_to_autofill = "button:has-text('Click to autofill')"
        self.btn_parsed = "button:has-text('Parsed')"

        # Job fields
        self.input_job_title = "input[name='position']"
        self.input_company_name = "input[placeholder='Search here']"
        self.input_location = "button:has-text('Hyderabad')"

        # Action buttons
        self.btn_publish = "button:has-text('Publish')"
        self.modal_success = "#custom-modal"
        self.btn_view_job = "button:has-text('View Job')"
        self.all_button = "#job-tablayout-parent"

        # ---------- WAIT CONFIG ----------
        self.default_timeout = 150000  # 150 seconds max wait for parsing

    # ---------- METHODS ----------

    def upload_document(self, file_path: str = JOB_FILE_PATH):
        """Upload a job description document (PDF, DOCX, TXT)."""
        self.logger.info(f"📁 Uploading document: {file_path}")
        self.page.set_input_files(self.input_upload_file, file_path)
        expect(self.page.locator(self.btn_click_to_autofill)).to_be_visible(timeout=10000)
        self.logger.info("✅ File uploaded successfully — 'Click to autofill' button visible.")

    def trigger_parsing(self):
        """Click the autofill button to trigger parsing."""
        self.logger.info("🧠 Clicking 'Click to autofill' to start parsing...")
        self.page.locator(self.btn_click_to_autofill).click()

    def wait_for_parsed_state(self):
        """Wait for the file to be parsed and form fields to be auto-filled."""
        self.logger.info("⏳ Waiting for parsing to complete (up to 150 seconds)...")
        expect(self.page.locator(self.btn_parsed)).to_be_visible(timeout=self.default_timeout)
        self.logger.info("✅ Parsing completed — 'Parsed' button visible (green).")



    def verify_autofilled_fields(self, job_title: str, company_name: str, location: str):
        """Verify that important fields are auto-filled correctly (partial match OK)."""
        self.logger.info("🔍 Verifying auto-filled fields after parsing (partial match)...")

        # Use regex for partial match
        expect(self.page.locator(self.input_job_title)).to_have_value(
            re.compile(job_title, re.IGNORECASE)
        )
        expect(self.page.locator(self.input_company_name)).to_have_value(
            re.compile(company_name, re.IGNORECASE)
        )

        # Location: partial text check
        location_element = self.page.locator(f"button:has-text('{location}')")
        expect(location_element).to_be_visible()

        self.logger.info(
            f"✅ Autofill validation passed (partial match) — Title includes: '{job_title}', Company includes: '{company_name}', Location: '{location}'"
        )


    def publish_job(self):
        """Click Publish to create the job."""
        self.logger.info("🚀 Clicking 'Publish' to create job post...")
        self.page.locator(self.btn_publish).click()

    def verify_success_modal(self, expected_text: str = SUCCESS_MESSAGE_JOB_CREATED):
        """Verify that the success modal is shown after publishing."""
        self.logger.info("⏳ Waiting for success modal after publish...")
        modal = self.page.locator(self.modal_success)
        expect(modal).to_contain_text(expected_text, timeout=20000)
        self.logger.info(f"🎉 Success modal verified — contains text: {expected_text}")

    def click_view_job(self):
        """Click 'View Job' on success modal."""
        self.logger.info("👁️ Clicking 'View Job' to open the job details page...")
        self.page.locator(self.btn_view_job).click()
        self.logger.info("✅ 'View Job' clicked successfully.")
        all_tab_button = self.page.locator(self.all_button).get_by_role("button", name="All")
        # Wait until visible
        expect(all_tab_button).to_be_visible(timeout=30000)
        # Now click safely
        all_tab_button.click()
        self.logger.info("✅ 'All' tab clicked successfully.")

        
