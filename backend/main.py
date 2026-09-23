from pathlib import Path

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.scrapers.amazon import scrape_amazon
from backend.database import SessionLocal
from backend.models import Product, ProductPrice
from backend.scrapers.flipkart import extract_flipkart_data
from backend.models import (
    Product,
    ProductPrice,
    Review,
    SentimentAnalysis,
    FakeReviewDetection
)


frontend_directory = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI(
    title="Intelligent Product Recommendation",
    description="AI-powered product comparison and recommendation system",
    version="1.0.0"
)

for static_folder in ["css", "js", "assets"]:
    folder_path = frontend_directory / static_folder
    folder_path.mkdir(parents=True, exist_ok=True)
    app.mount(f"/{static_folder}", StaticFiles(directory=folder_path), name=static_folder)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return FileResponse(frontend_directory / "index.html")


@app.post("/products")
def add_product(
    product_name: str,
    brand: str,
    category: str,
    db: Session = Depends(get_db)
):
    new_product = Product(
        product_name=product_name,
        brand=brand,
        category=category
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product added successfully",
        "product_id": new_product.product_id,
        "product_name": new_product.product_name
    }
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    return {
        "count": len(products),
        "products": [
            {
                "product_id": product.product_id,
                "product_name": product.product_name,
                "brand": product.brand,
                "category": product.category
            }
            for product in products
        ]
    }
@app.get("/products/search")
def search_products(
    name: str,
    db: Session = Depends(get_db)
):
    products = (
        db.query(Product)
        .filter(Product.product_name.ilike(f"%{name}%"))
        .all()
    )

    return {
        "count": len(products),
        "products": [
            {
                "product_id": product.product_id,
                "product_name": product.product_name,
                "brand": product.brand,
                "category": product.category,
                "image_url": product.image_url,
                "description": product.description
            }
            for product in products
        ]
    }
@app.get("/products/{product_id}/prices")
def get_product_prices(
    product_id: int,
    db: Session = Depends(get_db)
):
    prices = (
        db.query(ProductPrice)
        .filter(ProductPrice.product_id == product_id)
        .all()
    )

    return {
        "product_id": product_id,
        "count": len(prices),
        "prices": [
            {
                "website_name": price.website_name,
                "current_price": float(price.current_price)
                if price.current_price is not None else None,
                "original_price": float(price.original_price)
                if price.original_price is not None else None,
                "discount_percent": float(price.discount_percent)
                if price.discount_percent is not None else None,
                "availability": price.availability,
                "product_url": price.product_url
            }
            for price in prices
        ]
    }
@app.get("/products/{product_id}/review-analysis")
def get_review_analysis(
    product_id: int,
    db: Session = Depends(get_db)
):
    reviews = (
        db.query(Review)
        .filter(Review.product_id == product_id)
        .all()
    )

    if not reviews:
        return {
            "product_id": product_id,
            "review_count": 0,
            "sentiment_score": 0,
            "trust_score": 0,
            "positive_reviews": 0,
            "negative_reviews": 0,
            "neutral_reviews": 0
        }

    review_ids = [review.review_id for review in reviews]

    sentiments = (
        db.query(SentimentAnalysis)
        .filter(
            SentimentAnalysis.review_id.in_(review_ids)
        )
        .all()
    )

    fake_results = (
        db.query(FakeReviewDetection)
        .filter(
            FakeReviewDetection.review_id.in_(review_ids)
        )
        .all()
    )


    # ---------- SENTIMENT SCORE ----------

    positive = 0
    negative = 0
    neutral = 0

    sentiment_strength = []

    for result in sentiments:

        if result.sentiment == "Positive":
            positive += 1

        elif result.sentiment == "Negative":
            negative += 1

        else:
            neutral += 1

        if result.confidence_score is not None:
            sentiment_strength.append(
                float(result.confidence_score)
            )


    sentiment_score = (
        sum(sentiment_strength)
        / len(sentiment_strength)
        * 100
        if sentiment_strength
        else 0
    )


    # ---------- TRUST SCORE ----------

    genuine_probabilities = []

    for result in fake_results:

        if result.fake_score is not None:

            fake_probability = float(
                result.fake_score
            )

            genuine_probability = (
                1 - fake_probability
            )

            genuine_probabilities.append(
                genuine_probability
            )


    trust_score = (
        sum(genuine_probabilities)
        / len(genuine_probabilities)
        * 100
        if genuine_probabilities
        else 0
    )


    return {
        "product_id": product_id,
        "review_count": len(reviews),

        "sentiment_score":
            round(sentiment_score, 2),

        "trust_score":
            round(trust_score, 2),

        "positive_reviews":
            positive,

        "negative_reviews":
            negative,

        "neutral_reviews":
            neutral
    }

class ProductURLRequest(BaseModel):
    url: str


class AnalyzeQueryRequest(BaseModel):
    query: str


from backend.pipeline import run_full_recommendation_pipeline

@app.post("/api/analyze-full")
def analyze_full_pipeline(
    request: AnalyzeQueryRequest,
    db: Session = Depends(get_db)
):
    if not request.query or not request.query.strip():
        return {"status": "ERROR", "message": "Please provide a product URL or product name."}

    return run_full_recommendation_pipeline(request.query, db)


@app.post("/analyze-url")
def analyze_product_url(request: ProductURLRequest):

    domain = urlparse(request.url).netloc.lower()

    if "amazon." in domain:
        product = scrape_amazon(request.url)

    elif "flipkart." in domain:
        product = extract_flipkart_data(request.url)

    else:
        return {
            "message": "Unsupported website",
            "website": "Unsupported"
        }

    return {
        "message": f"{product.website} product scraped successfully",
        "website": product.website,
        "product_name": product.product_name,
        "current_price": product.current_price,
        "original_price": product.original_price,
        "discount_percent": product.discount_percent,
        "rating": product.rating,
        "review_count": product.review_count,
        "product_url": product.product_url,
        "availability": product.availability
    }