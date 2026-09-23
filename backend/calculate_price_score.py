from backend.database import SessionLocal
from backend.models import ProductPrice


def calculate_price_scores():

    db = SessionLocal()

    try:

        prices = db.query(ProductPrice).all()

        if not prices:
            print("No product prices found.")
            return

        lowest_price = min(
            float(price.current_price)
            for price in prices
        )

        print("\n========== PRICE SCORE ==========")
        print("Lowest Price:", lowest_price)

        for price in prices:

            current_price = float(
                price.current_price
            )

            price_score = (
                lowest_price / current_price
            ) * 100

            print(
                f"\nWebsite: {price.website_name}"
            )
            print(
                f"Price: ₹{current_price:.2f}"
            )
            print(
                f"Price Score: {price_score:.2f} / 100"
            )

        print("\n=================================")

    finally:
        db.close()


if __name__ == "__main__":
    calculate_price_scores()