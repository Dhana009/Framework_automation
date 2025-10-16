import pytest
from pages.login_page import LoginPage
from configs.config import BASE_URL, USERNAME, PASSWORD

@pytest.mark.smoke
def test_login_success(page):
    login_page = LoginPage(page)
    login_page.open_login_page(BASE_URL)
    login_page.login(USERNAME, PASSWORD)

    # Example validation: check if redirected or dashboard visible
    assert page.url.endswith("/dashboard"), "User not redirected to dashboard after login"
