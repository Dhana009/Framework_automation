from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Locators
        self.username_input = 'input[name="username"]'
        self.password_input = 'input[name="password"]'
        self.login_button = 'button[type="submit"]'
        self.error_message = '.error-message'

    # Actions
    def open_login_page(self, base_url):
        self.goto(f"{base_url}/login")

    def login(self, username, password):
        self.fill_text(self.username_input, username)
        self.fill_text(self.password_input, password)
        self.click_element(self.login_button)

    # Validation
    def get_error_message(self):
        return self.get_text(self.error_message)
