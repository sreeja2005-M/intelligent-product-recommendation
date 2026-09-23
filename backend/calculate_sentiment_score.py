from backend.database import SessionLocal
from backend.models import SentimentAnalysis


def calculate_sentiment_score():

    db = SessionLocal()

    try:

        results = db.query(SentimentAnalysis).all()

        if not results:
            print("No sentiment analysis records found.")
            return

        positive_count = 0
        negative_count = 0
        neutral_count = 0

        total_strength = 0.0

        for result in results:

            total_strength += float(
                result.confidence_score
            )

            if result.sentiment == "Positive":
                positive_count += 1

            elif result.sentiment == "Negative":
                negative_count += 1

            else:
                neutral_count += 1

        average_strength = (
            total_strength / len(results)
        )

        sentiment_score = average_strength * 100

        print("\n========== SENTIMENT SCORE ==========")
        print("Reviews analyzed:", len(results))

        print("Positive reviews:", positive_count)
        print("Negative reviews:", negative_count)
        print("Neutral reviews:", neutral_count)

        print(
            "Average Sentiment Strength:",
            round(average_strength, 4)
        )

        print(
            "Sentiment Score:",
            round(sentiment_score, 2),
            "/ 100"
        )

        print("=====================================")

    finally:
        db.close()


if __name__ == "__main__":
    calculate_sentiment_score()