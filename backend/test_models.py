from backend.database import engine
from backend.models import (
    User,
    Product,
    ProductPrice,
    Review,
    SentimentAnalysis,
    FakeReviewDetection,
    PriceHistory,
    FestivalOffer,
    Recommendation
)

print("✅ All 9 database models imported successfully!")

print("\nModels detected:")
print(User.__tablename__)
print(Product.__tablename__)
print(ProductPrice.__tablename__)
print(Review.__tablename__)
print(SentimentAnalysis.__tablename__)
print(FakeReviewDetection.__tablename__)
print(PriceHistory.__tablename__)
print(FestivalOffer.__tablename__)
print(Recommendation.__tablename__)

print("\n✅ Model configuration looks good!")