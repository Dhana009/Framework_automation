# pages/dashboard_page.py
from playwright.sync_api import Page, expect
from utils.logger import get_logger

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

        # Verified locators from dashboard.html
        self.post_new_job_button = page.locator('button:has-text("Post New Job")')
        self.view_all_jobs_button = page.locator('button:has-text("View All Jobs")')
        self.dashboard_root = page.locator('div.ant-layout')  # main dashboard container

    def is_loaded(self) -> bool:
        """Verify dashboard is visible after successful login."""
        try:
            expect(self.dashboard_root).to_be_visible(timeout=10000)
            expect(self.post_new_job_button).to_be_visible(timeout=10000)
            expect(self.view_all_jobs_button).to_be_visible(timeout=10000)
            self.logger.info("✅ Dashboard loaded successfully — buttons visible.")
            return True
        except Exception as e:
            self.logger.error(f"❌ Dashboard not loaded properly: {e}")
            # For debugging: print top part of DOM
            try:
                html_sample = self.page.inner_html("body")
                self.logger.error(f"DOM sample:\n{html_sample[:500]}")
            except Exception:
                pass
            return False
