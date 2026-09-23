from datetime import datetime

from backend.database import SessionLocal
from backend.models import Review, SentimentAnalysis
from backend.sentiment_analysis import analyze_sentiment


def analyze_and_save_sentiments():

    db = SessionLocal()

    try:

        reviews = db.query(Review).all()

        print("\n========== SENTIMENT ANALYSIS ==========")
        print("Reviews found:", len(reviews))

        saved_count = 0

        for review in reviews:

            sentiment, polarity = analyze_sentiment(
                review.review_text
            )

            # Convert polarity (-1 to +1)
            # into sentiment strength (0 to 100)
            confidence_score = abs(polarity)

            result = SentimentAnalysis(
                review_id=review.review_id,
                sentiment=sentiment,
                confidence_score=confidence_score,
                analyzed_at=datetime.now()
            )

            db.add(result)

            saved_count += 1

            print(
                f"\nReview ID: {review.review_id}"
            )
            print(
                f"Review: {review.review_text}"
            )
            print(
                f"Sentiment: {sentiment}"
            )
            print(
                f"Polarity: {polarity:.2f}"
            )
            print(
                f"Sentiment Strength: "
                f"{confidence_score:.4f}%"
            )

        db.commit()

        print(
            "\n========================================"
        )
        print(
            "Sentiment records saved:",
            saved_count
        )
        print(
            "========================================"
        )

    except Exception as e:

        db.rollback()

        print("\n❌ Sentiment save failed!")
        print("Error:", e)

    finally:

        db.close()


if __name__ == "__main__":
    analyze_and_save_sentiments()