# pages/login_page.py
from pages.base_page import BasePage
from playwright.sync_api import expect

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Verified locators from login page HTML
        self.email_input = 'input[type="email"]'
        self.password_input = 'input[type="password"]'
        self.signin_button = 'button:has-text("Sign in")'
        self.error_message = '.error-message, div[role="alert"]'

    def open_login_page(self, base_url: str):
        """Navigate to the login page"""
        # Ensures consistent navigation even if base_url has or lacks /login
        url = base_url.rstrip('/')
        if not url.endswith("/login"):
            url += "/login"
        self.goto(url)

    def login(self, email: str, password: str):
        """Perform login action"""
        self.fill_text(self.email_input, email)
        self.fill_text(self.password_input, password)
        self.click_element(self.signin_button)

    def get_error_message(self):
        """Retrieve the login error message (if visible)"""
        try:
            return self.get_text(self.error_message)
        except Exception:
            return ""
