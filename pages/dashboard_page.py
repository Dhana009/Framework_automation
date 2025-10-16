# pages/dashboard_page.py
from playwright.sync_api import Page, expect
from utils.logger import get_logger
import re

class DashboardPage:
    """Page Object for SproutsAI Dashboard Page"""

    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

        # ---------- TOP NAVIGATION BAR ----------
        self.global_search_input_primary = page.get_by_placeholder("Search for jobs or candidates...")
        self.global_search_input_fallback = page.locator('input[placeholder="Search for jobs or candidates..."]')

        self.category_dropdown_primary = page.locator('#category-dropdown button')
        self.category_dropdown_fallback = page.get_by_text("All", exact=False)

        self.post_new_job_button_primary = page.get_by_role("button", name="Post new job")
        self.post_new_job_button_fallbacks = [
            page.get_by_text("Post new job", exact=False),
            page.locator('button[class*="solid-button-blue"]'),
        ]

        self.notification_icon_primary = page.locator('span.relative > svg.cursor-pointer')
        self.notification_icon_fallback = page.locator('svg[viewBox="0 0 22 22"]')

        self.notification_badge_primary = page.locator('span.relative span[class*="rounded"][class*="bg-"]')
        self.notification_badge_fallback = page.locator('span.relative >> text=/^\\d+$/')

        self.profile_section_primary = page.locator('div.cursor-pointer.flex.rounded-md')
        self.profile_section_fallback = page.locator('div[style*="border-radius"]')

        self.user_avatar_primary = page.locator('div.text-white[style*="background-color"]')
        self.user_avatar_fallback = page.locator('div.flex.items-center.justify-center[style*="background-color"]')

        self.user_name_primary = page.locator('span.text-gray-800.font-semibold')
        self.user_name_fallback = page.get_by_text("dhanunjaya", exact=False)

        self.organization_name_primary = page.get_by_text("SproutsAI", exact=False)
        self.organization_name_fallback = page.locator('span:has-text("SproutsAI")')

        # ---------- LEFT SIDEBAR ----------
        self.sidebar_dashboard = page.locator('[data-tooltip-content="Dashboard"]')
        self.sidebar_job = page.locator('[data-tooltip-content="Job"]')
        self.sidebar_analytics = page.locator('[data-tooltip-content="Analytics Dashboard"]')
        self.sidebar_candidates = page.locator('[data-tooltip-content="Candidates Pool"]')
        self.sidebar_messages = page.locator('[data-tooltip-content="Messages"]')
        self.sidebar_companies = page.locator('[data-tooltip-content="Companies"]')
        self.sidebar_sequences = page.locator('[data-tooltip-content="Sequences"]')
        self.sidebar_templates = page.locator('[data-tooltip-content="Templates"]')
        self.sidebar_manage_org = page.locator('[data-tooltip-content="Manage Organization"]')

        # ---------- MAIN CONTENT ----------
        self.dashboard_heading_primary = page.locator('main >> text=Dashboard')
        self.dashboard_heading_fallback = page.get_by_text("Dashboard", exact=False)

        self.task_list_header_primary = page.get_by_text("Task list", exact=False)
        self.task_list_header_fallback = page.locator('span:has-text("Task list")')

        self.todays_interviews_primary = page.get_by_text("Today’s interviews", exact=False)
        self.todays_interviews_fallback = page.get_by_text("Today", exact=False)

    # ---------- UTILITY ----------
    def _get_visible_locator(self, *locators):
        """Return the first visible locator from a list"""
        for locator in locators:
            try:
                if locator.count() > 0:
                    return locator
            except Exception:
                continue
        raise Exception("❌ No visible locator found for this element")

    # ---------- ACTIONS ----------
    def is_dashboard_loaded(self) -> bool:
        """Verify dashboard is visible after login."""
        try:
            expect(self.post_new_job_button_primary).to_be_visible(timeout=30000)
            self.logger.info("✅ Dashboard loaded — 'Post New Job' button is visible.")
            return True
        except Exception as e:
            self.logger.error(f"❌ Dashboard not loaded: {e}")
            return False



    def click_post_new_job(self):
        locator = self._get_visible_locator(self.post_new_job_button_primary, *self.post_new_job_button_fallbacks)
        locator.click()
        self.logger.info("🖱️ Clicked on 'Post new job' button")

    def open_notifications(self):
        locator = self._get_visible_locator(self.notification_icon_primary, self.notification_icon_fallback)
        locator.click()
        self.logger.info("🔔 Opened notifications panel")

    def get_notification_count(self) -> int:
        """Returns the number from the notification badge"""
        locator = self._get_visible_locator(self.notification_badge_primary, self.notification_badge_fallback)
        text = locator.inner_text().strip()
        count = int(re.search(r'\d+', text).group()) if re.search(r'\d+', text) else 0
        self.logger.info(f"🔢 Notification count: {count}")
        return count

    def open_profile_menu(self):
        locator = self._get_visible_locator(self.profile_section_primary, self.profile_section_fallback)
        locator.click()
        self.logger.info("👤 Opened profile dropdown")

    def get_user_details(self) -> dict:
        """Fetches username and organization name"""
        username = self._get_visible_locator(self.user_name_primary, self.user_name_fallback).inner_text().strip()
        orgname = self._get_visible_locator(self.organization_name_primary, self.organization_name_fallback).inner_text().strip()
        self.logger.info(f"👤 User: {username}, Organization: {orgname}")
        return {"username": username, "organization": orgname}

    def search_for(self, keyword: str):
        locator = self._get_visible_locator(self.global_search_input_primary, self.global_search_input_fallback)
        locator.fill(keyword)
        locator.press("Enter")
        self.logger.info(f"🔎 Performed global search for: {keyword}")

    def navigate_to(self, section_name: str):
        """Navigate using sidebar tooltip name"""
        locator = self.page.locator(f'[data-tooltip-content="{section_name}"]')
        if locator.count() > 0:
            locator.click()
            self.logger.info(f"📂 Navigated to sidebar section: {section_name}")
        else:
            self.logger.warning(f"⚠️ Sidebar section not found: {section_name}")

    # ---------- VALIDATIONS ----------
    def verify_dashboard_title(self) -> bool:
        """Check that Dashboard heading is visible"""
        try:
            locator = self._get_visible_locator(self.dashboard_heading_primary, self.dashboard_heading_fallback)
            expect(locator).to_be_visible(timeout=5000)
            self.logger.info("✅ Dashboard title visible.")
            return True
        except Exception as e:
            self.logger.error(f"❌ Dashboard title not found: {e}")
            return False
