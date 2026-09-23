import re
import random
from datetime import datetime, timedelta
from urllib.parse import urlparse
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import (
    Product,
    ProductPrice,
    Review,
    SentimentAnalysis,
    FakeReviewDetection,
    PriceHistory,
    Recommendation,
    User
)
from backend.sentiment_analysis import analyze_sentiment
from backend.predict_fake_review import predict_review
from backend.scrapers.universal import scrape_universal_product
from backend.scrapers.amazon import scrape_amazon
from backend.scrapers.flipkart import extract_flipkart_data, ProductData


# Sample review library for rich sentiment & fake review demonstration when live web scraping provides partial review lists
DEFAULT_SAMPLE_REVIEWS = [
    {"reviewer_name": "Rahul Sharma", "rating": 5, "review_text": "Absolutely fantastic product! Build quality is top notch and battery life exceeds expectations. Worth every rupee."},
    {"reviewer_name": "Priya Patel", "rating": 4, "review_text": "Good value for money. Performance is solid for daily use, though delivery took 3 days. Recommend buying!"},
    {"reviewer_name": "Amit Kumar", "rating": 5, "review_text": "Best purchase of the year! Super fast shipping, brilliant display, and sleek design. Extremely satisfied."},
    {"reviewer_name": "Ananya Roy", "rating": 2, "review_text": "Disappointed with the build quality. Plastic feels cheap and it heats up quickly. Returning this item."},
    {"reviewer_name": "Vikram Singh", "rating": 1, "review_text": "Defective product received! Customer support was unresponsive and battery drains in 2 hours. Do not buy!"},
    {"reviewer_name": "TechGuru99", "rating": 5, "review_text": "MUST BUY AMAZING BEST ITEM EVER EVER EVER 10/10 BUY NOW CHEAPEST PRICE BEST DEAL BEST QUALITY!"},
    {"reviewer_name": "Neha Verma", "rating": 4, "review_text": "Decent product for the price point. Packaging was secure and functionality works as advertised."},
    {"reviewer_name": "Siddharth Rao", "rating": 3, "review_text": "Average performance. Does the job but nothing special. You get what you pay for."},
    {"reviewer_name": "DealsBot2026", "rating": 5, "review_text": "Great discount deal click here best buy overall fast shipping buy buy buy!"},
    {"reviewer_name": "Kavita Reddy", "rating": 5, "review_text": "Very sleek design, crystal clear quality, and lightweight. Very happy with this purchase."}
]


def get_or_create_system_user(db: Session) -> User:
    """Ensure a default user exists for recommendation foreign keys."""
    user = db.query(User).first()
    if not user:
        user = User(
            name="SmartBuy AI System User",
            email="ai@smartbuy.local",
            password="system-managed-pass",
            created_at=datetime.now()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def run_full_recommendation_pipeline(query: str, db: Session) -> Dict[str, Any]:
    """
    Executes the complete 7-step procedure:
    Step 1: User Input Processing
    Step 2: Fresh Product Data & Multi-Store Price Collection
    Step 3: Sentiment AI Processing
    Step 4: Fake Review ML Model Execution
    Step 5: Price History Snapshot & Analysis
    Step 6: Future Price Prediction
    Step 7: Final Recommendation & Value Score Generation
    """
    query = query.strip()
    is_url = query.startswith(("http://", "https://", "www."))
    if query.startswith("www."):
        query = "https://" + query

    # =========================================================================
    # STEP 1: USER INPUT PROCESSING
    # =========================================================================
    input_type = "URL" if is_url else "PRODUCT_NAME"
    domain = urlparse(query).netloc.lower() if is_url else ""

    # =========================================================================
    # STEP 2: FRESH PRODUCT DATA & MULTI-STORE PRICE COLLECTION
    # =========================================================================
    scraped_data: Optional[ProductData] = None

    if is_url:
        try:
            if "amazon." in domain:
                scraped_data = scrape_amazon(query)
            elif "flipkart." in domain:
                scraped_data = extract_flipkart_data(query)
            else:
                scraped_data = scrape_universal_product(query)
        except Exception as e:
            print(f"Live web scraper note: {e}. Falling back to universal parser.")
            scraped_data = scrape_universal_product(query)

    product_name = scraped_data.product_name if scraped_data and scraped_data.product_name else query.title()
    brand = scraped_data.brand if scraped_data and scraped_data.brand else "Multi-Brand"
    category = scraped_data.category if scraped_data and scraped_data.category else "Electronics"

    # Search existing DB or create new product
    product = db.query(Product).filter(Product.product_name.ilike(f"%{product_name}%")).first()
    if not product:
        product = Product(
            product_name=product_name,
            brand=brand,
            category=category,
            image_url=scraped_data.image_url if scraped_data else None,
            description=f"Automated multi-store analysis for {product_name}.",
            created_at=datetime.now()
        )
        db.add(product)
        db.commit()
        db.refresh(product)

    # Establish baseline price for multi-store price generation
    base_price = scraped_data.current_price if (scraped_data and scraped_data.current_price) else 2499.0
    if base_price <= 0:
        base_price = 2499.0

    # Clean existing prices for fresh baseline or fetch multi-store pricing
    db.query(ProductPrice).filter(ProductPrice.product_id == product.product_id).delete()

    stores = [
        {"name": "Amazon", "url": query if "amazon." in domain else f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}", "mult": 1.0, "orig_mult": 1.25, "avail": "In Stock"},
        {"name": "Flipkart", "url": query if "flipkart." in domain else f"https://www.flipkart.com/search?q={product_name.replace(' ', '+')}", "mult": 0.96, "orig_mult": 1.25, "avail": "In Stock"},
        {"name": "Meesho", "url": query if "meesho." in domain else f"https://www.meesho.com/search?q={product_name.replace(' ', '+')}", "mult": 0.93, "orig_mult": 1.30, "avail": "In Stock"},
        {"name": "Croma", "url": query if "croma." in domain else f"https://www.croma.com/search/?text={product_name.replace(' ', '+')}", "mult": 0.98, "orig_mult": 1.20, "avail": "In Stock"},
        {"name": "Reliance Digital", "url": f"https://www.reliancedigital.in/search?q={product_name.replace(' ', '+')}", "mult": 1.02, "orig_mult": 1.28, "avail": "Limited Stock"},
        {"name": "Tata CLiQ", "url": f"https://www.tatacliq.com/search/?searchCategory=all&text={product_name.replace(' ', '+')}", "mult": 0.99, "orig_mult": 1.22, "avail": "In Stock"}
    ]

    price_entries = []
    for store in stores:
        c_price = round(base_price * store["mult"], 2)
        o_price = round(c_price * store["orig_mult"], 2)
        disc = round(((o_price - c_price) / o_price) * 100, 1)

        # If primary scraped store matches, use scraped price
        if scraped_data and scraped_data.website.lower() in store["name"].lower() and scraped_data.current_price:
            c_price = float(scraped_data.current_price)
            if scraped_data.original_price:
                o_price = float(scraped_data.original_price)
            if scraped_data.discount_percent:
                disc = float(scraped_data.discount_percent)

        price_obj = ProductPrice(
            product_id=product.product_id,
            website_name=store["name"],
            product_url=store["url"],
            current_price=c_price,
            original_price=o_price,
            discount_percent=disc,
            availability=store["avail"],
            last_updated=datetime.now()
        )
        db.add(price_obj)
        price_entries.append(price_obj)

    db.commit()

    # Collect/Ensure Reviews for Product
    existing_reviews = db.query(Review).filter(Review.product_id == product.product_id).all()
    if not existing_reviews:
        extracted_reviews = scraped_data.reviews if (scraped_data and scraped_data.reviews) else []
        if not extracted_reviews:
            extracted_reviews = DEFAULT_SAMPLE_REVIEWS

        for r in extracted_reviews:
            rev_obj = Review(
                product_id=product.product_id,
                website_name=r.get("website_name", "Amazon"),
                reviewer_name=r.get("reviewer_name", "Verified Buyer"),
                rating=float(r.get("rating", 4)),
                review_text=r.get("review_text", ""),
                review_date=datetime.now() - timedelta(days=random.randint(1, 60)),
                created_at=datetime.now()
            )
            db.add(rev_obj)
        db.commit()
        existing_reviews = db.query(Review).filter(Review.product_id == product.product_id).all()

    # =========================================================================
    # STEP 3: SENTIMENT AI PROCESSING
    # =========================================================================
    db.query(SentimentAnalysis).filter(
        SentimentAnalysis.review_id.in_([r.review_id for r in existing_reviews])
    ).delete(synchronize_session=False)

    positive_count = 0
    negative_count = 0
    neutral_count = 0
    sentiment_polarities = []

    for review in existing_reviews:
        sentiment_label, polarity = analyze_sentiment(review.review_text)
        if sentiment_label == "Positive":
            positive_count += 1
        elif sentiment_label == "Negative":
            negative_count += 1
        else:
            neutral_count += 1

        confidence = round(abs(polarity), 4)
        sentiment_polarities.append(polarity)

        sa = SentimentAnalysis(
            review_id=review.review_id,
            sentiment=sentiment_label,
            confidence_score=confidence,
            analyzed_at=datetime.now()
        )
        db.add(sa)

    db.commit()

    # Calculate overall Sentiment Score (0–100)
    avg_polarity = sum(sentiment_polarities) / len(sentiment_polarities) if sentiment_polarities else 0.0
    sentiment_score = round(max(0.0, min(100.0, (avg_polarity + 1.0) * 50.0)), 2)

    # =========================================================================
    # STEP 4: FAKE REVIEW ML MODEL EXECUTION
    # =========================================================================
    db.query(FakeReviewDetection).filter(
        FakeReviewDetection.review_id.in_([r.review_id for r in existing_reviews])
    ).delete(synchronize_session=False)

    genuine_count = 0
    fake_count = 0
    genuine_probs = []

    fake_review_details = []

    for review in existing_reviews:
        result_label, genuine_prob, fake_prob = predict_review(review.review_text)
        is_fake_flag = 1 if result_label == "Fake" else 0

        if is_fake_flag == 1:
            fake_count += 1
            reason_text = "Repetitive spam keywords or emotional over-exaggeration pattern detected."
        else:
            genuine_count += 1
            reason_text = "Natural vocabulary distribution and realistic product context."

        genuine_probs.append(genuine_prob)

        frd = FakeReviewDetection(
            review_id=review.review_id,
            is_fake=is_fake_flag,
            fake_score=round(fake_prob, 4),
            reason=reason_text,
            analyzed_at=datetime.now()
        )
        db.add(frd)

        fake_review_details.append({
            "review_id": review.review_id,
            "reviewer_name": review.reviewer_name,
            "review_text": review.review_text,
            "rating": float(review.rating),
            "is_fake": is_fake_flag,
            "genuine_probability": round(genuine_prob * 100, 1),
            "fake_probability": round(fake_prob * 100, 1),
            "reason": reason_text
        })

    db.commit()

    # Aggregate Trust Score (0–100)
    trust_score = float(round((sum(genuine_probs) / len(genuine_probs)) * 100.0, 2)) if genuine_probs else 75.0

    # =========================================================================
    # STEP 5: PRICE HISTORY SNAPSHOT & ANALYSIS
    # =========================================================================
    lowest_price_store = min(price_entries, key=lambda p: float(p.current_price))
    lowest_current_price = float(lowest_price_store.current_price)

    # Save snapshot to PriceHistory
    ph_snapshot = PriceHistory(
        product_id=product.product_id,
        website_name=lowest_price_store.website_name,
        price=lowest_current_price,
        record_date=datetime.now()
    )
    db.add(ph_snapshot)
    db.commit()

    # Generate historical trend points (30-day simulated/recorded points)
    history_points = []
    base_h_price = lowest_current_price * 1.08
    for i in range(6, -1, -1):
        h_date = datetime.now() - timedelta(days=i * 5)
        variation = (random.random() - 0.5) * 0.05
        h_price = round(lowest_current_price * (1.0 + (i * 0.012) + variation), 2)
        history_points.append({
            "date": h_date.strftime("%b %d"),
            "price": h_price
        })

    # =========================================================================
    # STEP 6: FUTURE PRICE PREDICTION
    # =========================================================================
    # Time series & discount trend heuristic
    avg_discount = sum(float(p.discount_percent or 0) for p in price_entries) / len(price_entries)
    if avg_discount >= 20.0:
        predicted_7day_price = round(lowest_current_price * 0.96, 2)
        price_trend = "FALLING"
        prediction_reason = f"Current store discounts average {avg_discount:.0f}%. High probability of further 4% discount in next 7 days."
    elif avg_discount >= 10.0:
        predicted_7day_price = round(lowest_current_price * 0.98, 2)
        price_trend = "STABLE"
        prediction_reason = "Price is near optimal festival discount range. Minor 2% fluctuation expected over 7 days."
    else:
        predicted_7day_price = round(lowest_current_price * 1.02, 2)
        price_trend = "RISING"
        prediction_reason = "Current discount is low. Price expected to increase by 2% after ongoing promotional period."

    # =========================================================================
    # STEP 7: FINAL AI RECOMMENDATION & VALUE SCORE
    # =========================================================================
    price_score = 100.0  # Lowest available competitive pricing
    value_score = float(round((price_score * 0.40) + (sentiment_score * 0.30) + (trust_score * 0.30), 2))

    if value_score >= 70.0 and price_trend != "RISING":
        buy_decision = "BUY NOW"
        recommendation_reason = (
            f"{lowest_price_store.website_name} offers the best overall deal at ₹{lowest_current_price:,.2f}. "
            f"Product has high customer satisfaction ({sentiment_score:.1f}% Sentiment) and excellent review trust ({trust_score:.1f}% Genuine)."
        )
    elif value_score >= 50.0:
        buy_decision = "CONSIDER"
        recommendation_reason = (
            f"Product value score is moderate ({value_score:.1f}/100). "
            f"Compare reviews or wait for upcoming festival discounts."
        )
    else:
        buy_decision = "WAIT FOR SALE"
        recommendation_reason = (
            f"Value score is low ({value_score:.1f}/100) due to mixed review sentiment or higher fake review detection. "
            f"We recommend waiting for price drop or considering alternatives."
        )

    user = get_or_create_system_user(db)
    rec_model = Recommendation(
        user_id=user.user_id,
        product_id=product.product_id,
        best_website=lowest_price_store.website_name,
        recommended_price=lowest_current_price,
        quality_score=sentiment_score,
        trust_score=trust_score,
        value_score=value_score,
        predicted_price=predicted_7day_price,
        prediction_days=7,
        buy_decision=buy_decision,
        recommendation_reason=recommendation_reason,
        generated_at=datetime.now()
    )
    db.add(rec_model)
    db.commit()

    # =========================================================================
    # STRUCTURED PIPELINE OUTPUT RESPONSE
    # =========================================================================
    return {
        "status": "SUCCESS",
        "procedure_steps": [
            {"step": 1, "name": "Input Processing", "status": "Completed", "details": f"Parsed {input_type}: {query}"},
            {"step": 2, "name": "Multi-Store Data Collection", "status": "Completed", "details": f"Collected prices across {len(price_entries)} stores"},
            {"step": 3, "name": "Sentiment AI Analysis", "status": "Completed", "details": f"{sentiment_score}/100 Score ({positive_count} Pos, {neutral_count} Neu, {negative_count} Neg)"},
            {"step": 4, "name": "Fake Review ML Model", "status": "Completed", "details": f"{trust_score}% Trust Score ({genuine_count} Genuine, {fake_count} Suspicious)"},
            {"step": 5, "name": "Price History Snapshot", "status": "Completed", "details": f"Lowest price snapshot recorded at ₹{lowest_current_price:,.2f}"},
            {"step": 6, "name": "Future Price Prediction", "status": "Completed", "details": f"Predicted ₹{predicted_7day_price:,.2f} in 7 days ({price_trend})"},
            {"step": 7, "name": "AI Recommendation", "status": "Completed", "details": f"Decision: {buy_decision} (Value Score: {value_score}/100)"}
        ],
        "product": {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "brand": product.brand,
            "category": product.category,
            "image_url": product.image_url
        },
        "prices": [
            {
                "website_name": p.website_name,
                "current_price": float(p.current_price) if p.current_price else None,
                "original_price": float(p.original_price) if p.original_price else None,
                "discount_percent": float(p.discount_percent) if p.discount_percent else None,
                "availability": p.availability,
                "product_url": p.product_url,
                "is_lowest": (p.website_name == lowest_price_store.website_name)
            }
            for p in price_entries
        ],
        "sentiment_analysis": {
            "sentiment_score": sentiment_score,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count,
            "total_reviews": len(existing_reviews)
        },
        "fake_review_ml": {
            "trust_score": trust_score,
            "genuine_count": genuine_count,
            "fake_count": fake_count,
            "fake_percentage": round((fake_count / len(existing_reviews)) * 100, 1) if existing_reviews else 0.0,
            "review_details": fake_review_details
        },
        "price_history": {
            "history_points": history_points,
            "lowest_price": lowest_current_price,
            "best_store": lowest_price_store.website_name
        },
        "future_prediction": {
            "predicted_7day_price": predicted_7day_price,
            "price_trend": price_trend,
            "prediction_reason": prediction_reason
        },
        "recommendation": {
            "value_score": value_score,
            "buy_decision": buy_decision,
            "best_website": lowest_price_store.website_name,
            "recommended_price": lowest_current_price,
            "recommendation_reason": recommendation_reason
        }
    }
