import os
import pytest
import allure
from datetime import datetime
from playwright.sync_api import sync_playwright


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

    # Close page & context (finalizes video)
    page.close()
    context.close()

    video_path = page.video.path() if page.video else None

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

    # Screenshot on failure
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