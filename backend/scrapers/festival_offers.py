from playwright.sync_api import sync_playwright
from datetime import datetime
import re
import sys

from backend.database import SessionLocal
from backend.models import FestivalOffer


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


AMAZON_URL = (
    "https://www.amazon.in/Backpacks-50-Off-or-more-Bags/"
    "s?rh=n%3A2917430031%2Cp_n_pct-off-with-tax%3A2665401031"
)

FLIPKART_URL = (
    "https://www.flipkart.com/backpacks/pr?sid=reh,4d7,ak9"
)


def save_offer(
    website,
    price,
    discount
):
    db = SessionLocal()

    try:
        offer = FestivalOffer(
            product_id=None,
            website_name=website,
            festival_name="Current Sale",
            offer_start_date=datetime.now(),
            offer_end_date=None,
            discount_percent=discount,
            offer_price=price
        )

        db.add(offer)
        db.commit()

    except Exception as e:
        db.rollback()
        print("❌ Database save error:", e)

    finally:
        db.close()


def scrape_amazon(page):

    print("\n========== AMAZON OFFERS ==========")

    page.goto(
        AMAZON_URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    page.wait_for_timeout(4000)

    products = page.locator(
        'div[data-component-type="s-search-result"]'
    )

    count = min(products.count(), 10)

    print("Products found:", count)

    for i in range(count):

        try:

            item = products.nth(i)

            # Product name
            name = item.locator("h2").last.inner_text().strip()

            # Current price
            price_text = item.locator(
                ".a-price-whole"
            ).first.inner_text()

            price = float(
                re.sub(r"[^\d]", "", price_text)
            )

            # Complete product text
            text = item.inner_text()

            # MRP
            mrp = None

            mrp_match = re.search(
                r"M\.R\.P:\s*₹?([\d,]+)",
                text
            )

            if mrp_match:
                mrp = float(
                    mrp_match.group(1).replace(",", "")
                )

            # Discount
            discount = None

            discount_match = re.search(
                r"\((\d+)% off\)",
                text
            )

            if discount_match:
                discount = float(
                    discount_match.group(1)
                )

            print(f"\n{i + 1}. {name}")
            print(f"Price: ₹{price}")

            if mrp:
                print(f"MRP: ₹{mrp}")

            if discount:
                print(f"Discount: {discount}%")

                # Save to MySQL
                save_offer(
                    website="Amazon",
                    price=price,
                    discount=discount
                )

                print("✅ Saved to database")

        except Exception as e:

            print(
                f"⚠️ Could not process Amazon product {i + 1}:",
                e
            )


def scrape_flipkart(page):

    print("\n========== FLIPKART OFFERS ==========")

    page.goto(
        FLIPKART_URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    page.wait_for_timeout(4000)

    cards = page.locator("div[data-id]")

    count = min(cards.count(), 10)

    print("Products found:", count)

    for i in range(count):

        try:

            card = cards.nth(i)

            text = card.inner_text()

            lines = [
                x.strip()
                for x in text.split("\n")
                if x.strip()
            ]

            if not lines:
                continue

            # Product name
            name = lines[1] if len(lines) > 1 else lines[0]

            # Prices
            discount_text = None

            for span_text in card.locator("span").all_inner_texts():
                if re.fullmatch(r"\d+%\s*off", span_text.strip()):
                    discount_text = span_text.strip()
                    break

            discount_match = (
                re.search(r"(\d+)%\s*off", discount_text)
                if discount_text
                else None
            )

            price_text = (
                text.replace(discount_text, "")
                if discount_text
                else text
            )

            prices = re.findall(r"₹[\d,]+", price_text)

            if not prices:
                continue

            # Current price
            current_price = float(
                prices[0]
                .replace("₹", "")
                .replace(",", "")
            )

            # Original price
            original_price = None

            if len(prices) > 1:

                original_price = float(
                    prices[1]
                    .replace("₹", "")
                    .replace(",", "")
                )

            # Discount
            discount = None

            if discount_match:

                discount = float(
                    discount_match.group(1)
                )

            print(f"\n{i + 1}. {name}")
            print(f"Price: ₹{current_price}")

            if original_price:
                print(
                    f"MRP: ₹{original_price}"
                )

            if discount:
                print(
                    f"Discount: {discount}%"
                )

                # Save to MySQL
                save_offer(
                    website="Flipkart",
                    price=current_price,
                    discount=discount
                )

                print("✅ Saved to database")

        except Exception as e:

            print(
                f"⚠️ Could not process Flipkart product {i + 1}:",
                e
            )


def main():

    print("\n======================================")
    print(" FESTIVAL / SALE OFFER SCRAPER")
    print("======================================")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        # Amazon
        scrape_amazon(page)

        # Flipkart
        scrape_flipkart(page)

        browser.close()

    print("\n======================================")
    print("✅ SCRAPING COMPLETED")
    print("======================================")


if __name__ == "__main__":
    main()