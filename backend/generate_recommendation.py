from datetime import datetime

from backend.database import SessionLocal
from backend.models import Recommendation, ProductPrice, User


def get_recommendation_user(db):
    user = db.query(User).order_by(User.user_id).first()

    if user is not None:
        return user

    user = User(
        name="CLI Recommendation User",
        email="cli-recommendation@local",
        password="not-used-by-cli",
        created_at=datetime.now()
    )
    db.add(user)
    db.flush()
    return user


def generate_recommendation():

    db = SessionLocal()

    try:
        prices = db.query(ProductPrice).all()

        if not prices:
            print("No price data found.")
            return

        # Existing project scores
        sentiment_score = 58.19
        trust_score = 37.43

        lowest_price = min(float(p.current_price) for p in prices)

        best = None

        for price in prices:

            if price.current_price is None or float(price.current_price) <= 0:
                continue

            current_price = float(price.current_price)

            price_score = (
                lowest_price / current_price
            ) * 100

            value_score = (
                price_score * 0.40
                + sentiment_score * 0.30
                + trust_score * 0.30
            )

            if best is None or value_score > best["value_score"]:
                best = {
                    "product_id": price.product_id,
                    "website": price.website_name,
                    "price": current_price,
                    "price_score": price_score,
                    "value_score": value_score
                }

        if best is None:
            print("No valid price data found.")
            return

        user = get_recommendation_user(db)

        # Current project decision
        buy_decision = "BUY NOW"

        reason = (
            f"{best['website']} has the best overall value score "
            f"based on price, sentiment and review trust. "
            f"Current price is ₹{best['price']:.2f}."
        )

        recommendation = Recommendation(
            user_id=user.user_id,
            product_id=best["product_id"],
            best_website=best["website"],
            recommended_price=best["price"],
            quality_score=sentiment_score,
            trust_score=trust_score,
            value_score=best["value_score"],
            predicted_price=best["price"],
            prediction_days=0,
            buy_decision=buy_decision,
            recommendation_reason=reason,
            generated_at=datetime.now()
        )

        db.add(recommendation)
        db.commit()
        db.refresh(recommendation)

        print("\n========== FINAL RECOMMENDATION ==========")
        print("Recommendation ID:", recommendation.recommendation_id)
        print("Website:", best["website"])
        print(f"Recommended Price: ₹{best['price']:.2f}")
        print(f"Quality Score: {sentiment_score:.2f}")
        print(f"Trust Score: {trust_score:.2f}")
        print(f"Value Score: {best['value_score']:.2f}")
        print("Decision:", buy_decision)
        print("Reason:", reason)
        print("==========================================")

    finally:
        db.close()


if __name__ == "__main__":
    generate_recommendation()