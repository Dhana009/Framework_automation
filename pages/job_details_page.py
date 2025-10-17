# pages/job_details_page.py

import time
from playwright.sync_api import Page, expect
from utils.logger import get_logger
from configs.test_data import JOB_FILE_PATH, JOB_DETAILS
from configs.constants import SUCCESS_MESSAGE_JOB_CREATED
from configs.config import normal_timeout
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


        # ---------- SCREENING QUESTION SELECTORS ----------
        self.btn_background_check = page.get_by_role("button", name="Background check")
        self.btn_industry_experience = page.get_by_role("button", name="Industry experience")
        self.btn_visa_status = page.get_by_role("button", name="Visa status")
        self.btn_work_authorization = page.get_by_role("button", name="Work authorization")
        self.btn_remote_work = page.get_by_role("button", name="Remote work")
        self.btn_add_custom_question = page.get_by_role("button", name="Add custom question")

        self.question_1 = page.get_by_role("button", name="Question 1")
        self.question_2 = page.get_by_role("button", name="Question 2")
        self.question_3 = page.get_by_role("button", name="Question 3")
        self.question_4 = page.get_by_role("button", name="Question 4")
        self.question_5 = page.get_by_role("button", name="Question 5")
        self.question_6 = page.get_by_role("button", name="Question 6")
        self.question_7 = page.get_by_role("button", name="Question 7")
        self.custom_question_8 = page.get_by_role("button", name="Custom question 8")
        self.custom_question_9 = page.get_by_role("button", name="Custom question 9")

        self.text_question_8 = page.locator(".w-full.py-4 > div:nth-child(2) > .w-\\[100\\%\\]").first
        self.text_question_9 = page.locator("div:nth-child(9) > .w-full.py-4 > div:nth-child(2) > .w-\\[100\\%\\]")
        self.checkbox_required_7 = page.locator("#required7")
        self.dropdown_answer_type_8 = page.locator("#answerType8")

        # ---------- WAIT CONFIG ----------
        self.default_timeout = 150000  # 150 seconds max wait for parsing

    # ---------- EXISTING METHODS (DO NOT TOUCH) ----------

    def upload_document(self, file_path: str = JOB_FILE_PATH):
        """Upload a job description document (PDF, DOCX, TXT)."""
        self.logger.info(f"📁 Uploading document: {file_path}")
        self.page.set_input_files(self.input_upload_file, file_path)
        expect(self.page.locator(self.btn_click_to_autofill)).to_be_visible(timeout=normal_timeout)
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

        expect(self.page.locator(self.input_job_title)).to_have_value(
            re.compile(job_title, re.IGNORECASE)
        )
        expect(self.page.locator(self.input_company_name)).to_have_value(
            re.compile(company_name, re.IGNORECASE)
        )

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
        expect(all_tab_button).to_be_visible(timeout=30000)
        all_tab_button.click()
        self.logger.info("✅ 'All' tab clicked successfully.")

    # =====================================================================
    # 🔥 NEW METHODS ADDED BELOW — FOR EDIT / UPDATE / PREVIEW / PUBLISH 🔥
    # =====================================================================

    def open_edit_mode(self):
        """Open existing job in edit mode."""
        self.logger.info("🖊️ Opening existing job for editing...")
        self.page.locator(".border-button.inline-flex.text-center").click()
        self.page.get_by_text("Edit").click()
        expect(self.page.get_by_role("heading", name="Create or Upload Job")).to_be_visible(timeout=normal_timeout)
        self.logger.info("✅ Edit job page loaded.")

    def fill_basic_job_details(self, position, internal_title, headcount):
        """Fill position, internal title, and headcount."""
        self.logger.info("✏️ Filling job basic details...")
        self.page.locator("input[name='position']").fill(position)
        self.page.locator("#internal-job-title").fill(internal_title)
        self.page.locator("#headcount").fill(str(headcount))
        self.logger.info("✅ Basic job details filled.")


    def add_job_type_and_department(self, job_type, department):
        """Add job type and department tags."""
        self.logger.info("🏷️ Adding job type and department...")
        self.page.locator("#Job-type").get_by_role("textbox", name="Type here").fill(job_type)
        self.page.keyboard.press("Enter")
        expect(self.page.get_by_role("button", name=job_type, exact=True)).to_be_visible(timeout=normal_timeout)

        self.page.get_by_role("button", name="Full-time").click()
        self.page.get_by_role("textbox", name="Department").fill(department)
        self.page.keyboard.press("Enter")
        expect(self.page.get_by_role("button", name=department, exact=True)).to_be_visible(timeout=normal_timeout)
        self.logger.info("✅ Job type and department added.")

    def select_location(self, location_name):
        """Select location from dropdown search."""
        self.logger.info(f"📍 Selecting location: {location_name}")
        self.page.get_by_role("button", name="On-site").click()
        self.page.get_by_role("textbox", name="Press Enter to insert").fill(location_name)
        self.page.wait_for_selector(f"text={location_name}", state="visible", timeout=normal_timeout)
        self.page.get_by_text(location_name, exact=True).click()
        expect(self.page.get_by_role("button", name=location_name)).to_be_visible(timeout=normal_timeout)
        self.logger.info(f"✅ Location '{location_name}' selected.")

    def fill_salary_details(self, min_salary, max_salary, currency, duration, note):
        """Fill salary and note fields."""
        self.logger.info("💰 Filling salary and compensation details...")
        self.page.locator("select[name='expectedSalaryCurrency']").select_option(currency)
        self.page.locator("input[name='expectedSalaryMin']").fill(str(min_salary))
        self.page.locator("input[name='expectedSalaryMax']").fill(str(max_salary))
        self.page.locator("select[name='expectedSalaryDuration']").select_option(duration)
        self.page.get_by_role("textbox", name="Enter your salary note").fill(note)
        self.logger.info("✅ Salary details filled successfully.")

    def preview_job(self):
        """Click preview and verify sections."""
        self.logger.info("🧾 Previewing job...")
        self.page.get_by_role("button", name="Preview").click()
        expect(self.page.get_by_role("heading", name="Description")).to_be_visible(timeout=normal_timeout)
        expect(self.page.get_by_text(re.compile("₹.*Per day"))).to_be_visible(timeout=normal_timeout)
        self.logger.info("✅ Preview verified.")

    def publish_updated_job(self):
        """Publish the updated job and verify success."""
        self.logger.info("🚀 Publishing updated job...")
        self.page.get_by_role("button", name="Publish").click()
        expect(
            self.page.get_by_role("heading", name=re.compile("Job (Created|Updated) Successfully!", re.IGNORECASE))
        ).to_be_visible(timeout=60000)
        self.logger.info("✅ Job updated successfully.")

    def view_published_job(self):
        """View job after publish."""
        self.logger.info("👁️ Viewing published job...")
        self.page.get_by_role("button", name="View Job").click()
        expect(self.page.get_by_role("button", name=re.compile("Active", re.IGNORECASE))).to_be_visible(timeout=normal_timeout)
        self.logger.info("✅ Job view confirmed.")


    # ---------- SCREENING QUESTION METHODS ----------

    def enable_default_screening_questions(self):
        """Enable each default question and verify they appear in sequence."""
        self.logger.info("🧩 Enabling default screening questions...")

        mapping = [
            (self.btn_background_check, self.question_1),
            (self.btn_industry_experience, self.question_3),
            (self.btn_visa_status, self.question_5),
            (self.btn_work_authorization, self.question_6),
            (self.btn_remote_work, self.question_7),
        ]

        for button, question in mapping:
            button.click()
            expect(question).to_be_visible(timeout=normal_timeout)
            self.logger.info(f"✅ Enabled question: {button} -> Verified: {question}")

    def add_custom_screening_questions(self):
        """Add and fill two custom questions."""
        self.logger.info("➕ Adding custom screening questions...")

        self.btn_add_custom_question.click()
        expect(self.custom_question_8).to_be_visible(timeout=normal_timeout)

        self.btn_add_custom_question.click()
        expect(self.custom_question_9).to_be_visible(timeout=normal_timeout)

        self.text_question_8.fill("testing 8")
        self.checkbox_required_7.check()
        self.text_question_9.fill("testing 9")
        self.dropdown_answer_type_8.select_option("link")

        self.logger.info("✅ Custom questions added and filled.")
