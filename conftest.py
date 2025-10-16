import os
import pytest
import allure
from datetime import datetime
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    """Launch a single browser instance per session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        yield browser
        browser.close()


@pytest.fixture()
def page(browser, request):
    """
    Provide a fresh context + page for each test.
    Adds video recording, screenshots on failure, and Allure attachments.
    """
    # Isolated browser context per test
    context = browser.new_context(record_video_dir="videos/")
    page = context.new_page()

    # Global default timeouts
    page.set_default_timeout(60000)
    context.set_default_timeout(60000)

    yield page  # test runs here

    # ---- Teardown: handle failures ----
    test_name = request.node.name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    video_path = None
    if page.video:
        video_path = page.video.path()

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        # Save screenshot
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = f"screenshots/{test_name}_{timestamp}.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"🖼 Screenshot saved: {screenshot_path}")

        # Attach screenshot to Allure (if reporting is enabled)
        if request.config.getoption("--alluredir", None):
            allure.attach.file(
                screenshot_path,
                name=f"{test_name}_failure",
                attachment_type=allure.attachment_type.PNG
            )

        # Attach video to Allure
        if video_path and os.path.exists(video_path):
            allure.attach.file(
                video_path,
                name=f"{test_name}_video",
                attachment_type=allure.attachment_type.MP4
            )

    page.close()
    context.close()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Hook to set test outcome (pass/fail) on request.node for fixtures."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
