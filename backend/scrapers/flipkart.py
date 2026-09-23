from playwright.sync_api import sync_playwright
import re

from backend.scrapers.base import ProductData


def extract_flipkart_data(url):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        print("Opening Flipkart page...")

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(3000)

        print("Page title:", page.title())
        print("Current URL:", page.url)

        body_text = page.locator("body").inner_text()

        # --------------------------------
        # PRODUCT NAME
        # --------------------------------

        # --------------------------------
        # PRODUCT NAME
        # --------------------------------

        product_name = None

        name_selectors = [
            "span.VU-ZEz",
            "span.B_NuCI",
            "h1._6EBuvT",
            "h1"
        ]

        for selector in name_selectors:
            try:
                element = page.locator(selector).first

                if element.count() > 0:
                    text = element.inner_text().strip()

                    if text:
                        product_name = text
                        break

            except Exception:
                continue

        # --------------------------------
        # CURRENT PRICE
        # --------------------------------

        current_price = None

        price_selectors = [
            "div.Nx9bqj",
            "div._30jeq3",
            "div.Nx9bqj._4b5DiR",
            "div._16Jk6d"
        ]

        for selector in price_selectors:
            try:
                elements = page.locator(selector)

                for i in range(elements.count()):
                    text = elements.nth(i).inner_text().strip()

                    match = re.search(
                        r"₹\s*([\d,]+(?:\.\d{1,2})?)",
                        text
                    )

                    if match:
                        current_price = float(
                            match.group(1).replace(",", "")
                        )
                        break

                if current_price is not None:
                    break

            except Exception:
                continue
        # Flipkart currently renders the product summary as discount, MRP,
        # and selling price on separate lines without stable CSS classes.
        summary_match = re.search(
            r"(?P<discount>\d{1,2})%\s*\n"
            r"(?P<original>[\d,]+)\s*\n"
            r"₹\s*(?P<current>[\d,]+(?:\.\d{1,2})?)",
            body_text
        )

        original_price = None
        discount_percent = None

        if summary_match:
            original_price = float(
                summary_match.group("original").replace(",", "")
            )
            discount_percent = float(summary_match.group("discount"))
            current_price = float(
                summary_match.group("current").replace(",", "")
            )

        # A product with no ratings is reported as zero instead of null.
        rating = 0.0
        review_count = 0

        rating_match = re.search(
            r"Ratings and reviews.*?(\d(?:\.\d)?)\s*\|\s*([\d,]+)",
            body_text,
            re.DOTALL
        )

        if rating_match:
            rating = float(rating_match.group(1))
            review_count = int(rating_match.group(2).replace(",", ""))

        # --------------------------------
        # PRODUCT DATA
        # --------------------------------

        product = ProductData(
            website="Flipkart",
            product_name=product_name,
            current_price=current_price,
            original_price=original_price,
            discount_percent=discount_percent,
            rating=rating,
            review_count=review_count,
            product_url=page.url,
            availability="Available"
        )

        # --------------------------------
        # DISPLAY RESULT
        # --------------------------------

        print("\n========== FLIPKART PRODUCT DATA ==========")

        print("Website:", product.website)
        print("Product Name:", product.product_name)
        print("Current Price:", product.current_price)
        print("Original Price:", product.original_price)
        print("Discount Percent:", product.discount_percent)
        print("Rating:", product.rating)
        print("Review Count:", product.review_count)
        print("Product URL:", product.product_url)

        print("============================================")

        browser.close()

        return product


if __name__ == "__main__":

    url = input(
        "Enter Flipkart product URL: "
    ).strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    extract_flipkart_data(url)