from playwright.sync_api import sync_playwright
import re

from backend.scrapers.base import ProductData


def extract_price(page):
    selectors = [
        "#corePrice_feature_div .a-price .a-offscreen",
        "#corePriceDisplay_desktop_feature_div .a-price .a-offscreen",
        "#apex_desktop .a-price .a-offscreen",
        "#priceblock_ourprice",
        "#priceblock_dealprice",
    ]

    for selector in selectors:
        elements = page.locator(selector)

        if elements.count() > 0:
            for i in range(elements.count()):
                text = elements.nth(i).get_attribute("textContent")

                if text:
                    match = re.search(
                        r"₹\s*([\d,]+(?:\.\d{1,2})?)",
                        text
                    )

                    if match:
                        return float(
                            match.group(1).replace(",", "")
                        )

    # Fallback
    product_area = page.locator("#centerCol")

    if product_area.count() > 0:
        price_elements = product_area.locator(".a-price")

        for i in range(price_elements.count()):
            try:
                text = price_elements.nth(i).inner_text()

                match = re.search(
                    r"₹\s*([\d,]+(?:\.\d{1,2})?)",
                    text
                )

                if match:
                    return float(
                        match.group(1).replace(",", "")
                    )

            except:
                continue

    return None


def extract_original_price(page):

    product_area = page.locator("#centerCol")

    if product_area.count() == 0:
        return None

    text = product_area.inner_text()

    match = re.search(
        r"M\.?R\.?P\.?\s*:?\s*₹\s*([\d,]+(?:\.\d{1,2})?)",
        text,
        re.IGNORECASE
    )

    if match:
        return float(
            match.group(1).replace(",", "")
        )

    return None


def extract_discount_percent(page):

    product_area = page.locator("#centerCol")

    if product_area.count() == 0:
        return None

    text = product_area.inner_text()

    match = re.search(
        r"(\d+)\s*percent\s*savings",
        text,
        re.IGNORECASE
    )

    if match:
        return float(match.group(1))

    return None


def scrape_amazon(url):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        print("Opening Amazon page...")

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(3000)

        print("Page title:", page.title())
        print("Current URL:", page.url)

        # Product name
        product_name = page.locator(
            "#productTitle"
        ).first.inner_text().strip()

        # Current price
        current_price = extract_price(page)

        # Original price
        original_price = extract_original_price(page)

        # Discount
        discount_percent = extract_discount_percent(page)

        # Create common ProductData object
        product = ProductData(
            website="Amazon",
            product_name=product_name,
            current_price=current_price,
            original_price=original_price,
            discount_percent=discount_percent,
            product_url=page.url,
        )

        browser.close()

        return product


if __name__ == "__main__":

    url = input(
        "Enter Amazon product URL: "
    ).strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    result = scrape_amazon(url)

    print("\n========== AMAZON PRODUCT DATA ==========")

    print("Website:", result.website)
    print("Product Name:", result.product_name)
    print("Current Price:", result.current_price)
    print("Original Price:", result.original_price)
    print("Discount Percent:", result.discount_percent)
    print("Product URL:", result.product_url)

    print("==========================================")