from playwright.sync_api import sync_playwright


url = "https://www.croma.com/preethi-cocosta-coconut-scraper-citrus-juicer-black-/p/274212"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    print("Opening Croma page...")

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    page.wait_for_timeout(5000)

    print("\n========== CROMA PRODUCT ==========")

    print("Page Title:", page.title())

    # Get visible page text
    text = page.locator("body").inner_text()

    print("\n--- Page Content Preview ---")
    print(text[:5000])

    print("\n===================================")

    browser.close()