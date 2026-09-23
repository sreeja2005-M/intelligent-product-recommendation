import json
import re

from playwright.sync_api import sync_playwright


def _json_ld_product(page):
    for script in page.locator('script[type="application/ld+json"]').all():
        try:
            data = json.loads(script.text_content() or "")
        except json.JSONDecodeError:
            continue

        entries = data if isinstance(data, list) else [data]
        for entry in entries:
            if isinstance(entry, dict) and entry.get("@type") == "Product":
                return entry

    return {}


def _first_match(pattern, text, flags=re.IGNORECASE):
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else None


def scrape_croma(url):
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/139.0.0.0 Safari/537.36"
            ),
            locale="en-IN"
        )

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        text = page.locator("body").inner_text()

        if "Access Denied" in page.title() or "Access Denied" in text:
            browser.close()
            raise RuntimeError(
                "Croma blocked the automated browser request (Access Denied)."
            )

        product = _json_ld_product(page)
        offers = product.get("offers", {})
        rating_data = product.get("aggregateRating", {})

        product_name = product.get("name") or _first_match(
            r"(?:^|\n)([^\n]*Preethi Cocosta[^\n]*)", text
        )
        current_price = offers.get("price")
        original_price = _first_match(
            r"(?:MRP|Maximum Retail Price)\s*:?\s*(₹\s*[\d,]+(?:\.\d{2})?)",
            text
        )
        discount_percent = _first_match(r"(\d+(?:\.\d+)?%)\s*off", text)
        rating = rating_data.get("ratingValue") or _first_match(
            r"(?:rating|rated)\s*[:\-]?\s*([0-5](?:\.\d+)?)", text
        )
        review_count = rating_data.get("reviewCount") or rating_data.get("ratingCount") or _first_match(
            r"([\d,]+)\s*(?:reviews?|ratings?)", text
        )

        if current_price is not None:
            current_price = f"₹{float(current_price):,.2f}"

        browser.close()

        return {
            "website": "Croma",
            "product_name": product_name,
            "current_price": current_price,
            "original_price": original_price,
            "discount_percent": discount_percent,
            "rating": rating,
            "review_count": review_count,
            "url": url
        }