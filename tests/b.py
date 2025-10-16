import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://test.app.sproutsai.com/login")

    #dashboard text check
    page.get_by_text("Dashboard").click()
    #visibility check
    expect(page.get_by_role("button", name="Post new job")).to_be_visible()

    #post new job button click
    page.get_by_role("button", name="Post new job").click()
    expect(page.get_by_role("heading", name="Create or Upload Job")).to_be_visible()

    #generate with ai is visible
    expect(page.get_by_role("button", name="Generate with AI")).to_be_visible()
    #upload the file
    page.set_input_files("input#upload", r"D:\automation playwright\framework\Framework_automation\tests\🌟 Software Test Engineer – SproutsAI.pdf")
    expect(page.get_by_role("button", name="Click to autofill")).to_be_visible()

    #check remove is working or not
    page.get_by_text("Remove").click()
    expect(page.get_by_text("Drag or click to browse your")).to_be_visible()
    page.set_input_files("input#upload", r"D:\automation playwright\framework\Framework_automation\tests\🌟 Software Test Engineer – SproutsAI.pdf")
    expect(page.get_by_role("button", name="Click to autofill")).to_be_visible()
    #click the button and 
    page.get_by_role("button", name="Click to autofill").click()

    #wait for max 120 to 150 seconds for the parsing to be completed
    expect(page.get_by_role("button", name="Parsed")).to_be_visible()

    #except job name to be same
    expect(page.locator("input[name=\"position\"]")).to_have_value("Software")

    #company name
    expect(page.get_by_role("textbox", name="Search here")).to_have_value("SproutsAI")

    #location
    page.get_by_role("button", name="Hyderabad").is_visible()

    #publish
    page.get_by_role("button", name="Publish").click()
    
    #successfull modal
    expect(page.locator("#custom-modal")).to_contain_text("Job Created Successfully!")
    #view jobs
    page.get_by_role("button", name="View Job").click()

    page.locator("#job-tablayout-parent").get_by_role("button", name="All").click()