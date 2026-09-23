from backend.database import SessionLocal
from backend.models import ProductPrice


def calculate_value_score():
    db = SessionLocal()

    try:
        prices = db.query(ProductPrice).all()

        if not prices:
            print("No price data found.")
            return

        # Price score
        lowest_price = min(float(p.current_price) for p in prices)

        price_scores = []

        for p in prices:
            current_price = float(p.current_price)
            price_score = (lowest_price / current_price) * 100
            price_scores.append((p.website_name, price_score, current_price))

        # Existing AI scores
        sentiment_score = 58.19
        trust_score = 37.43

        print("\n========== VALUE SCORE ==========")

        for website, price_score, current_price in price_scores:

            # Overall Value Score
            value_score = (
                price_score * 0.40
                + sentiment_score * 0.30
                + trust_score * 0.30
            )

            print(f"\nWebsite: {website}")
            print(f"Price: ₹{current_price:.2f}")
            print(f"Price Score: {price_score:.2f} / 100")
            print(f"Sentiment Score: {sentiment_score:.2f} / 100")
            print(f"Trust Score: {trust_score:.2f} / 100")
            print(f"Value Score: {value_score:.2f} / 100")

        print("\n=================================")

    finally:
        db.close()


if __name__ == "__main__":
    calculate_value_score()