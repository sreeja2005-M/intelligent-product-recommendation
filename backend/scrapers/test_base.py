from backend.scrapers.base import ProductData


product = ProductData(
    website="Croma",
    product_name="Preethi Cocosta Coconut Scraper & Citrus Juicer",
    current_price=4199,
    original_price=6449,
    discount_percent=34.89,
    rating=4.0,
    review_count=1,
    product_url="https://www.croma.com/",
    availability="Not Available"
)

print(product)