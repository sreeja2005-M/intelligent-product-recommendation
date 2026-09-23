from backend.database import SessionLocal
from backend.models import FakeReviewDetection


def calculate_trust_score():

    db = SessionLocal()

    try:

        results = db.query(FakeReviewDetection).all()

        if not results:
            print("No fake review detection records found.")
            return

        genuine_probabilities = [
            1 - float(result.fake_score)
            for result in results
        ]

        average_genuine_probability = (
            sum(genuine_probabilities)
            / len(genuine_probabilities)
        )

        trust_score = average_genuine_probability * 100

        print("\n========== TRUST SCORE ==========")
        print("Reviews analyzed:", len(results))

        print(
            "Average Genuine Probability:",
            round(average_genuine_probability, 4)
        )

        print(
            "Trust Score:",
            round(trust_score, 2),
            "/ 100"
        )

        print("=================================")

    finally:
        db.close()


if __name__ == "__main__":
    calculate_trust_score()