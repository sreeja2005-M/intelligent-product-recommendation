from backend.scrapers.amazon import scrape_amazon
from backend.scrapers.flipkart import extract_flipkart_data


def compare_prices(amazon_url, flipkart_url):

    print("\n🔄 Scraping Amazon...")
    amazon_product = scrape_amazon(amazon_url)

    print("\n🔄 Scraping Flipkart...")
    flipkart_product = extract_flipkart_data(flipkart_url)

    products = [
        amazon_product,
        flipkart_product
    ]

    print("\n========== PRICE COMPARISON ==========")

    for product in products:

        print(
            f"{product.website}: "
            f"₹{product.current_price}"
        )

    # Remove products where price wasn't extracted
    valid_products = [
        product
        for product in products
        if product.current_price is not None
    ]

    if not valid_products:
        print("\n❌ No valid prices found.")
        return

    # Find lowest current price
    best_product = min(
        valid_products,
        key=lambda product: product.current_price
    )

    print("\n--------------------------------------")

    print(
        "Best Current Price:",
        best_product.website
    )

    print(
        "Price:",
        f"₹{best_product.current_price}"
    )

    print("--------------------------------------")

    # Show price difference
    if len(valid_products) > 1:

        highest_price = max(
            product.current_price
            for product in valid_products
        )

        price_difference = (
            highest_price
            - best_product.current_price
        )

        print(
            "Maximum Price Difference:",
            f"₹{price_difference:.2f}"
        )

    print("======================================\n")


if __name__ == "__main__":

    amazon_url = input(
        "Enter Amazon product URL: "
    ).strip()

    flipkart_url = input(
        "Enter Flipkart product URL: "
    ).strip()

    if not amazon_url.startswith(
        ("http://", "https://")
    ):
        amazon_url = "https://" + amazon_url

    if not flipkart_url.startswith(
        ("http://", "https://")
    ):
        flipkart_url = "https://" + flipkart_url

    compare_prices(
        amazon_url,
        flipkart_url
    )