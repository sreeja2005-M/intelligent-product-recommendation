from textblob import TextBlob


def analyze_sentiment(review_text):

    blob = TextBlob(review_text)

    polarity = blob.sentiment.polarity

    if polarity > 0:
        sentiment = "Positive"

    elif polarity < 0:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return sentiment, polarity


if __name__ == "__main__":

    review = input(
        "Enter a review: "
    ).strip()

    sentiment, polarity = analyze_sentiment(review)

    print("\n========== SENTIMENT RESULT ==========")
    print("Review:", review)
    print("Sentiment:", sentiment)
    print("Polarity:", round(polarity, 2))
    print("======================================")