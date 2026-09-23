from backend.database import SessionLocal
from backend.models import ProductPrice

db = SessionLocal()

try:
    new_price = ProductPrice(
        product_id=2,
        website_name="Flipkart",
        product_url="https://www.flipkart.com/",
        current_price=1239.00,
        original_price=3499.00,
        discount_percent=65.00,
        availability="Available"
    )

    db.add(new_price)
    db.commit()

    print("✅ Flipkart price saved successfully!")
    print("Price: ₹1239")
    print("Original Price: ₹3499")
    print("Discount: 65%")

finally:
    db.close()