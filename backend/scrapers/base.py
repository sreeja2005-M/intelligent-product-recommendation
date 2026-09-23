from dataclasses import dataclass
from typing import Optional


@dataclass
class ProductData:
    website: str
    product_name: Optional[str] = None
    current_price: Optional[float] = None
    original_price: Optional[float] = None
    discount_percent: Optional[float] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    product_url: Optional[str] = None
    availability: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    reviews: Optional[list] = None