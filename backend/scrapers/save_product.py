from backend.database import SessionLocal
from backend.models import Product, ProductPrice
from backend.scrapers.amazon import scrape_amazon


def save_amazon_product(url):

    # 1. Scrape Amazon
    product_data = scrape_amazon(url)

    db = SessionLocal()

    try:
        # 2. Check whether product already exists
        product = (
            db.query(Product)
            .filter(
                Product.product_name == product_data.product_name
            )
            .first()
        )

        # 3. If product doesn't exist, create it
        if product is None:

            product = Product(
                product_name=product_data.product_name,
                brand="Safari",
                category="Backpack"
            )

            db.add(product)
            db.commit()
            db.refresh(product)

            print("New product created.")
            print("Product ID:", product.product_id)

        else:
            print("Existing product found.")
            print("Product ID:", product.product_id)

        # 4. Save Amazon price
        price = ProductPrice(
            product_id=product.product_id,
            website_name=product_data.website,
            product_url=product_data.product_url,
            current_price=product_data.current_price,
            original_price=product_data.original_price,
            discount_percent=product_data.discount_percent,
            availability="Available"
        )

        db.add(price)
        db.commit()
        db.refresh(price)

        print("\n========== DATABASE SAVE RESULT ==========")
        print("Product ID:", product.product_id)
        print("Price ID:", price.price_id)
        print("Website:", price.website_name)
        print("Current Price:", price.current_price)
        print("Original Price:", price.original_price)
        print("Discount:", price.discount_percent)
        print("==========================================")

    except Exception as e:

        db.rollback()

        print("\n❌ Database save failed!")
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":

    url = input(
        "Enter Amazon product URL: "
    ).strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    save_amazon_product(url)