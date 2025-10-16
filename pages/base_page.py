import time
from playwright.sync_api import Page, expect
from utils.logger import get_logger



class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.page.set_default_timeout(60000)
        self.logger = get_logger(self.__class__.__name__)

    # Navigation
    def goto(self, url: str):
        """Navigate to a given URL."""
        self.page.goto(url)

    # Basic interactions
    def click_element(self, selector: str):
        """Click an element."""
        self.page.click(selector)

    def fill_text(self, selector: str, text: str):
        """Fill text into an input field."""
        self.page.fill(selector, text)

    def get_text(self, selector: str) -> str:
        """Return visible text of an element."""
        return self.page.inner_text(selector)

    def clear_text(self, selector: str):
        """Clear text before filling."""
        self.page.fill(selector, "")

    # Visibility and waiting
    def wait_for_element(self, selector: str, state="visible"):
        """Wait for an element to be in a specific state."""
        self.page.wait_for_selector(selector, state=state)

    def is_element_visible(self, selector: str) -> bool:
        """Check if an element is visible."""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=2000)
            return True
        except:
            return False

    def wait_for_timeout(self, seconds: float):
        """Hard wait (use sparingly)."""
        time.sleep(seconds)

    # Dropdowns
    def select_option(self, selector: str, value: str):
        """Select from a dropdown by value."""
        self.page.select_option(selector, value=value)

    # Hovering
    def hover_over_element(self, selector: str):
        """Hover over an element."""
        self.page.hover(selector)

    # Scrolling
    def scroll_into_view(self, selector: str):
        """Scroll until the element is in view."""
        self.page.locator(selector).scroll_into_view_if_needed()

    # Assertions (simple, handy for small validations)
    def expect_element_to_have_text(self, selector: str, text: str):
        """Assert element has given text."""
        expect(self.page.locator(selector)).to_have_text(text)

    def expect_element_to_be_visible(self, selector: str):
        """Assert element is visible."""
        expect(self.page.locator(selector)).to_be_visible()

    # File uploads
    def upload_file(self, selector: str, file_path: str):
        """
        Upload a file to an <input type='file'> element.
        Example usage:
            self.upload_file('input[type="file"]', 'tests/data/sample.pdf')
        """
        self.page.set_input_files(selector, file_path)

    # Keyboard actions
    def press_key(self, key: str):
        """Press a keyboard key (like 'Enter' or 'Escape')."""
        self.page.keyboard.press(key)
