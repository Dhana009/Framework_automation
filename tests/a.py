import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://test.app.sproutsai.com/login")

    page.get_by_text("Dashboard").click()
    page.get_by_role("button", name="Post new job").click()
    expect(page.get_by_role("heading", name="Create or Upload Job")).to_be_visible()
    
    page.get_by_role("heading", name="Create or upload new job post").click()
    page.set_input_files("input#upload", r"D:\automation playwright\framework\Framework_automation\tests\🌟 Software Test Engineer – SproutsAI.pdf")
    expect(page.get_by_role("button", name="Click to autofill")).to_be_visible()

    page.get_by_text("Remove").click()
    page.locator(".bg-\\[\\#33348e0a\\]").click()
    page.locator("body").set_input_files("🌟 Software Test Engineer – SproutsAI.pdf")
    page.get_by_role("button", name="Click to autofill").click()
    page.get_by_role("button", name="Parsed").click()
    page.get_by_text("Company detailsCompany").click()
    page.locator("#companySection").get_by_text("Company Name").click()
    page.get_by_role("textbox", name="Search here").click()
    expect(page.get_by_role("img", name="SproutsAI").first).to_be_visible()

    page.get_by_role("listitem").filter(has_text="Add Company SproutsAI").click()
    page.get_by_role("textbox", name="Enter company name").click()
    page.get_by_role("textbox", name="Enter company name").fill("SproutsAi")
    page.get_by_role("textbox", name="Enter company URL").click()
    page.get_by_role("textbox", name="Enter company URL").fill("sproutsai.com")
    page.get_by_role("button", name="Save", exact=True).click()
    expect(page.get_by_role("heading", name="SproutsAI", exact=True)).to_be_visible()

    page.locator("#field-established_year").get_by_title("Edit").click()
    page.locator("#field-established_year").get_by_role("textbox").fill("2023")
    page.get_by_role("button", name="Update").click()
    page.get_by_text("2023").click()
    page.locator("#custom-modal").get_by_role("button").filter(has_text=re.compile(r"^$")).click()
    page.get_by_role("button", name="View", exact=True).click()
    page.get_by_role("heading", name="SproutsAI", exact=True).click()
    page.locator("#custom-modal").get_by_role("button").filter(has_text=re.compile(r"^$")).click()
    page.get_by_role("button", name="Preview").click()
    expect(page.get_by_role("heading", name="Description")).to_be_visible()

    page.get_by_role("button", name="Publish").click()
    expect(page.get_by_role("heading", name="Job Created Successfully!")).to_be_visible()

    page.locator("div").filter(has_text=re.compile(r"^Software Test EngineerSproutsAI$")).first.click()
    page.get_by_role("heading", name="Job Created Successfully!").click()
    page.get_by_role("button", name="View Job").click()
    expect(page.get_by_role("button", name="Active (57)")).to_be_visible()

    page.get_by_text("LocationHyderabad, RajahmundryWorkplace typeOnsite, RemoteHeadcount1Experience0").click()
    page.locator("div").filter(has_text=re.compile(r"^AllDetailsAnalyticsAI-Tuned Profiles$")).first.click()
    page.get_by_text("Must haveIs preferredIs not").click()
