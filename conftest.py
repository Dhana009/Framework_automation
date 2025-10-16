import os
import pytest
import allure
from datetime import datetime
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect
# conftest.py (add this fixture)

import pytest
from pages.login_page import LoginPage
from configs.config import BASE_URL, USERNAME, PASSWORD, USERS

@pytest.fixture(scope="function")
def logged_in_page(page):
    """Reusable fixture that logs in before each test and yields an authenticated page."""
    login_page = LoginPage(page)
    login_page.open_login_page(BASE_URL)
    login_page.login(USERNAME, PASSWORD)
    yield page



def pytest_addoption(parser):
    parser.addoption(
        "--myvideo",
        action="store",
        default="retain-on-failure",
        choices=["on", "off", "retain-on-failure"],
        help="Video recording mode: on (always), off (never), retain-on-failure (default)"
    )


@pytest.fixture(scope="session")
def browser():
    """Launch a single browser instance per session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        yield browser
        browser.close()


@pytest.fixture()
def page(browser, request):
    video_mode = request.config.getoption("--myvideo")

    # Enable video recording only if requested
    record_video_dir = None if video_mode == "off" else "videos/"
    context = browser.new_context(record_video_dir=record_video_dir)
    page = context.new_page()

    # Timeouts
    page.set_default_timeout(60000)
    context.set_default_timeout(60000)

    yield page

    # -------- Teardown --------
    test_name = request.node.name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Screenshot BEFORE closing page/context
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = f"screenshots/{test_name}_{timestamp}.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"[Screenshot] Saved: {screenshot_path}")

        if request.config.getoption("--alluredir", None):
            allure.attach.file(
                screenshot_path,
                name=f"{test_name}_failure",
                attachment_type=allure.attachment_type.PNG
            )

    # Save video path reference BEFORE closing
    video_path = page.video.path() if page.video else None

    # Now close page & context (this finalizes the video file)
    page.close()
    context.close()

    # Handle video AFTER closing (file is finalized now)
    if video_mode == "on":
        if video_path and os.path.exists(video_path):
            print(f"[Video] Saved for test {test_name}: {video_path}")
            allure.attach.file(
                video_path,
                name=f"{test_name}_video",
                attachment_type=allure.attachment_type.MP4
            )

    elif video_mode == "retain-on-failure":
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            if video_path and os.path.exists(video_path):
                print(f"[Video] Retained for FAILED test {test_name}: {video_path}")
                allure.attach.file(
                    video_path,
                    name=f"{test_name}_video",
                    attachment_type=allure.attachment_type.MP4
                )
        else:
            # Clean up passed test videos
            if video_path and os.path.exists(video_path):
                os.remove(video_path)



@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Hook to set test outcome (pass/fail) on request.node for fixtures."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


#Always record videos (for every test):
# pytest --video=on

# Only record videos for failed tests (default):
# pytest --video=retain-on-failure

# Turn off video recording completely:
# pytest --video=off


@pytest.fixture(scope="session")
def multi_user_contexts(browser):
    """
    Logs in multiple users once per session.
    Returns a dict: {'RECRUITER': {'context': ctx, 'page': page}, ...}
    """
    from pages.login_page import LoginPage
    from configs.config import USERS, BASE_URL

    user_pages = {}

    for role, creds in USERS.items():
        context = browser.new_context(record_video_dir="videos/")
        page = context.new_page()
        page.set_default_timeout(60000)
        context.set_default_timeout(60000)
        

        login_page = LoginPage(page)
        login_page.open_login_page(BASE_URL)
        login_page.login(creds["username"], creds["password"])

        user_pages[role] = {"context": context, "page": page}
        print(f"[LOGIN] ✅ Logged in as {role} ({creds['username']})")

    yield user_pages

    # Teardown
    for role, items in user_pages.items():
        try:
            items["page"].close()
            items["context"].close()
            print(f"[LOGOUT] Closed session for {role}")
        except Exception as e:
            print(f"[WARNING] Could not close context for {role}: {e}")


@pytest.fixture(scope="function")
def get_user_page(multi_user_contexts):
    """
    Access any logged-in user's page.
    Example:
        def test_recruiter(get_user_page):
            page = get_user_page("RECRUITER")
    """
    def _get(role: str):
        role = role.upper()
        if role not in multi_user_contexts:
            raise ValueError(f"❌ Invalid role '{role}'. Available: {list(multi_user_contexts.keys())}")
        return multi_user_contexts[role]["page"]

    return _get