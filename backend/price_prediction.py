from backend.database import SessionLocal
from backend.models import FestivalOffer


def predict_offer_price():
    db = SessionLocal()

    try:
        offers = (
            db.query(FestivalOffer)
            .order_by(FestivalOffer.offer_price.asc())
            .all()
        )

        if not offers:
            print("No festival offers found.")
            return

        print("\n========== CURRENT OFFER ANALYSIS ==========")

        for offer in offers[:10]:
            price = float(offer.offer_price)
            discount = float(offer.discount_percent)

            # Simple market-based prediction signal
            if discount >= 75:
                decision = "BUY NOW"
                prediction = price
                reason = "High current discount detected."
            elif discount >= 60:
                decision = "BUY NOW"
                prediction = price
                reason = "Good current discount detected."
            else:
                decision = "WAIT"
                prediction = price
                reason = "Current discount is relatively low."

            print(f"\nWebsite: {offer.website_name}")
            print(f"Offer Price: ₹{price:.2f}")
            print(f"Discount: {discount:.0f}%")
            print(f"Predicted Price: ₹{prediction:.2f}")
            print(f"Decision: {decision}")
            print(f"Reason: {reason}")

        print("\n============================================")

    finally:
        db.close()


if __name__ == "__main__":
    predict_offer_price()