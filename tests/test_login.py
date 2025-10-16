# tests/test_login.py
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from configs.config import BASE_URL, USERNAME, PASSWORD

@pytest.mark.sanity
def test_login_success(page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    # Step 1: Open the login page
    login_page.open_login_page(BASE_URL)

    # Step 2: Enter credentials and login
    login_page.login(USERNAME, PASSWORD)

    # Step 3: Verify dashboard is loaded successfully
    assert dashboard_page.is_loaded(), "Login failed — Dashboard not visible."
