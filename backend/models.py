from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, DECIMAL, ForeignKey
from backend.database import Base


# ============================================================
# 1. USERS
# ============================================================

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(20))
    created_at = Column(TIMESTAMP)


# ============================================================
# 2. PRODUCTS
# ============================================================

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(255), nullable=False)
    brand = Column(String(100))
    category = Column(String(100))
    image_url = Column(String(500))
    description = Column(Text)
    specifications = Column(Text)
    created_at = Column(TIMESTAMP)


# ============================================================
# 3. PRODUCT PRICES
# ============================================================

class ProductPrice(Base):
    __tablename__ = "product_prices"

    price_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False
    )
    website_name = Column(String(100), nullable=False)
    product_url = Column(String(500))
    current_price = Column(DECIMAL(10, 2))
    original_price = Column(DECIMAL(10, 2))
    discount_percent = Column(DECIMAL(5, 2))
    availability = Column(String(50))
    last_updated = Column(TIMESTAMP)


# ============================================================
# 4. REVIEWS
# ============================================================

class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False
    )
    website_name = Column(String(100))
    reviewer_name = Column(String(100))
    rating = Column(DECIMAL(2, 1))
    review_text = Column(Text)
    review_date = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)


# ============================================================
# 5. SENTIMENT ANALYSIS
# ============================================================

class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analysis"

    sentiment_id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column(
        Integer,
        ForeignKey("reviews.review_id"),
        nullable=False
    )
    sentiment = Column(String(30))
    confidence_score = Column(DECIMAL(5, 2))
    analyzed_at = Column(TIMESTAMP)


# ============================================================
# 6. FAKE REVIEW DETECTION
# ============================================================

class FakeReviewDetection(Base):
    __tablename__ = "fake_review_detection"

    fake_id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column(
        Integer,
        ForeignKey("reviews.review_id"),
        nullable=False
    )
    is_fake = Column(Integer, nullable=False)
    fake_score = Column(DECIMAL(5, 4))
    reason = Column(Text)
    analyzed_at = Column(TIMESTAMP)


# ============================================================
# 7. PRICE HISTORY
# ============================================================

class PriceHistory(Base):
    __tablename__ = "price_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False
    )
    website_name = Column(String(100))
    price = Column(DECIMAL(10, 2))
    record_date = Column(TIMESTAMP)


# ============================================================
# 8. FESTIVAL OFFERS
# ============================================================

class FestivalOffer(Base):
    __tablename__ = "festival_offers"

    offer_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(
        Integer,
        ForeignKey("products.product_id", ondelete="SET NULL"),
        nullable=True
    )
    website_name = Column(String(100))
    festival_name = Column(String(100))
    offer_start_date = Column(TIMESTAMP)
    offer_end_date = Column(TIMESTAMP)
    discount_percent = Column(DECIMAL(5, 2))
    offer_price = Column(DECIMAL(10, 2))
    created_at = Column(TIMESTAMP)


# ============================================================
# 9. RECOMMENDATIONS
# ============================================================

class Recommendation(Base):
    __tablename__ = "recommendations"

    recommendation_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id", ondelete="CASCADE"),
        nullable=False
    )

    best_website = Column(String(100))
    recommended_price = Column(DECIMAL(10, 2))
    quality_score = Column(DECIMAL(5, 2))
    trust_score = Column(DECIMAL(5, 2))
    value_score = Column(DECIMAL(5, 2))
    predicted_price = Column(DECIMAL(10, 2))
    prediction_days = Column(Integer)
    buy_decision = Column(String(50), nullable=False)
    recommendation_reason = Column(Text)
    generated_at = Column(TIMESTAMP)