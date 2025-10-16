import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://test.app.sproutsai.com/login');
  await expect(page.getByRole('button', { name: 'LinkedIn' })).toBeVisible();

  await page.getByRole('textbox', { name: 'Enter Email' }).click();
  await page.getByRole('textbox', { name: 'Enter Email' }).fill('dhanunjaya@sproutsai.com');
  await page.getByRole('textbox', { name: 'Password' }).click();
  await page.getByRole('textbox', { name: 'Password' }).fill('Demo@123');
  await page.locator('path').nth(1).click();
  await page.getByRole('button', { name: 'Sign in' }).click();
  await expect(page.getByRole('button', { name: 'All', exact: true })).toBeVisible();

  await page.getByText('Dashboard').click();
  await page.getByRole('button', { name: 'Post new job' }).click();
  await expect(page.getByRole('heading', { name: 'Create or Upload Job' })).toBeVisible();

  await page.getByRole('heading', { name: 'Create or upload new job post' }).click();
  await page.locator('.bg-\\[\\#33348e0a\\]').click();
  await page.locator('body').setInputFiles('🌟 Software Test Engineer – SproutsAI.pdf');
  await expect(page.getByRole('button', { name: 'Click to autofill' })).toBeVisible();

  await page.getByText('Remove').click();
  await page.locator('.bg-\\[\\#33348e0a\\]').click();
  await page.locator('body').setInputFiles('🌟 Software Test Engineer – SproutsAI.pdf');
  await page.getByRole('button', { name: 'Click to autofill' }).click();
  await page.getByRole('button', { name: 'Parsed' }).click();
  await page.getByText('Company detailsCompany').click();
  await page.locator('#companySection').getByText('Company Name').click();
  await page.getByRole('textbox', { name: 'Search here' }).click();
  await expect(page.getByRole('img', { name: 'SproutsAI' }).first()).toBeVisible();

  await page.getByRole('listitem').filter({ hasText: 'Add Company SproutsAI' }).click();
  await page.getByRole('textbox', { name: 'Enter company name' }).click();
  await page.getByRole('textbox', { name: 'Enter company name' }).fill('SproutsAi');
  await page.getByRole('textbox', { name: 'Enter company URL' }).click();
  await page.getByRole('textbox', { name: 'Enter company URL' }).fill('sproutsai.com');
  await page.getByRole('button', { name: 'Save', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'SproutsAI', exact: true })).toBeVisible();

  await page.locator('#field-established_year').getByTitle('Edit').click();
  await page.locator('#field-established_year').getByRole('textbox').fill('2023');
  await page.getByRole('button', { name: 'Update' }).click();
  await page.getByText('2023').click();
  await page.locator('#custom-modal').getByRole('button').filter({ hasText: /^$/ }).click();
  await page.getByRole('button', { name: 'View', exact: true }).click();
  await page.getByRole('heading', { name: 'SproutsAI', exact: true }).click();
  await page.locator('#custom-modal').getByRole('button').filter({ hasText: /^$/ }).click();
  await page.getByRole('button', { name: 'Preview' }).click();
  await expect(page.getByRole('heading', { name: 'Description' })).toBeVisible();

  await page.getByRole('button', { name: 'Publish' }).click();
  await expect(page.getByRole('heading', { name: 'Job Created Successfully!' })).toBeVisible();

  await page.locator('div').filter({ hasText: /^Software Test EngineerSproutsAI$/ }).first().click();
  await page.getByRole('heading', { name: 'Job Created Successfully!' }).click();
  await page.getByRole('button', { name: 'View Job' }).click();
  await expect(page.getByRole('button', { name: 'Active (57)' })).toBeVisible();

  await page.getByText('LocationHyderabad, RajahmundryWorkplace typeOnsite, RemoteHeadcount1Experience0').click();
  await page.locator('div').filter({ hasText: /^AllDetailsAnalyticsAI-Tuned Profiles$/ }).first().click();
  await page.getByText('Must haveIs preferredIs not').click();
});