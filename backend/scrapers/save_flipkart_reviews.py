from backend.database import SessionLocal
from backend.models import Review
from backend.scrapers.flipkart_reviews import scrape_flipkart_reviews


def save_reviews(product_id, url):

    reviews = scrape_flipkart_reviews(url)

    db = SessionLocal()

    try:

        saved_count = 0

        for review_data in reviews:

            new_review = Review(
                product_id=product_id,
                website_name=review_data["website_name"],
                reviewer_name=review_data["reviewer_name"],
                rating=review_data["rating"],
                review_text=review_data["review_text"]
            )

            db.add(new_review)
            saved_count += 1

        db.commit()

        print("\n========== DATABASE SAVE ==========")
        print("Product ID:", product_id)
        print("Reviews saved:", saved_count)
        print("===================================")

    except Exception as e:

        db.rollback()

        print("\n❌ Database save failed!")
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":

    product_id = int(
        input("Enter Product ID: ").strip()
    )

    url = input(
        "Enter Flipkart product URL: "
    ).strip()

    if not url.startswith(
        ("http://", "https://")
    ):
        url = "https://" + url

    save_reviews(
        product_id,
        url
    )