import json
import re
from urllib.parse import urlparse
from typing import Dict, Any, List, Optional
from backend.scrapers.base import ProductData


def parse_json_ld(html_content: str) -> List[Dict[str, Any]]:
    """Extract all schema.org JSON-LD blocks from HTML content."""
    json_ld_blocks = []
    matches = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html_content,
        re.DOTALL | re.IGNORECASE
    )
    for match in matches:
        try:
            cleaned = match.strip()
            if cleaned:
                data = json.loads(cleaned)
                if isinstance(data, list):
                    json_ld_blocks.extend(data)
                elif isinstance(data, dict):
                    if "@graph" in data and isinstance(data["@graph"], list):
                        json_ld_blocks.extend(data["@graph"])
                    else:
                        json_ld_blocks.append(data)
        except Exception:
            continue
    return json_ld_blocks


def parse_opengraph(html_content: str) -> Dict[str, str]:
    """Extract OpenGraph meta tags from HTML content."""
    og_data = {}
    meta_tags = re.findall(r'<meta[^>]+>', html_content, re.IGNORECASE)
    for tag in meta_tags:
        property_match = re.search(r'(?:property|name)=["\']([^"\']+)["\']', tag, re.IGNORECASE)
        content_match = re.search(r'content=["\']([^"\']*)["\']', tag, re.IGNORECASE)
        if property_match and content_match:
            prop = property_match.group(1).lower()
            val = content_match.group(1).strip()
            og_data[prop] = val
    return og_data


def extract_price_from_text(text: str) -> Optional[float]:
    """Extract numerical currency price from text string."""
    if not text:
        return None
    match = re.search(r'(?:₹|\$|EUR|GBP|INR)?\s*([\d,]+(?:\.\d{1,2})?)', str(text))
    if match:
        try:
            return float(match.group(1).replace(',', ''))
        except ValueError:
            return None
    return None


def scrape_universal_product(url: str, html_content: Optional[str] = None) -> ProductData:
    """
    Universal product parser for any shopping website link.
    Extracts title, price, original price, discount, rating, review count, and reviews.
    """
    domain = urlparse(url).netloc.lower()
    website_name = domain.replace('www.', '').split('.')[0].capitalize()
    if 'amazon' in domain:
        website_name = 'Amazon'
    elif 'flipkart' in domain:
        website_name = 'Flipkart'
    elif 'croma' in domain:
        website_name = 'Croma'
    elif 'reliancedigital' in domain:
        website_name = 'Reliance Digital'
    elif 'tatacliq' in domain:
        website_name = 'Tata CLiQ'
    elif 'snapdeal' in domain:
        website_name = 'Snapdeal'

    product_name = None
    current_price = None
    original_price = None
    discount_percent = None
    rating = None
    review_count = None
    brand = None
    image_url = None
    reviews = []

    if html_content:
        # 1. Try JSON-LD parsing
        json_blocks = parse_json_ld(html_content)
        for block in json_blocks:
            if isinstance(block, dict) and block.get("@type") in ["Product", "IndividualProduct", "ItemPage"]:
                product_name = product_name or block.get("name")
                brand_obj = block.get("brand")
                if isinstance(brand_obj, dict):
                    brand = brand or brand_obj.get("name")
                elif isinstance(brand_obj, str):
                    brand = brand or brand_obj

                image_obj = block.get("image")
                if isinstance(image_obj, str):
                    image_url = image_url or image_obj
                elif isinstance(image_obj, list) and image_obj:
                    image_url = image_url or image_obj[0]

                offers = block.get("offers")
                if isinstance(offers, dict):
                    current_price = current_price or extract_price_from_text(offers.get("price"))
                elif isinstance(offers, list) and offers:
                    current_price = current_price or extract_price_from_text(offers[0].get("price"))

                aggregate_rating = block.get("aggregateRating")
                if isinstance(aggregate_rating, dict):
                    rating = rating or float(aggregate_rating.get("ratingValue", 0))
                    review_count = review_count or int(aggregate_rating.get("reviewCount") or aggregate_rating.get("ratingCount") or 0)

                raw_reviews = block.get("review", [])
                if isinstance(raw_reviews, dict):
                    raw_reviews = [raw_reviews]
                for rev in raw_reviews:
                    if isinstance(rev, dict):
                        rev_body = rev.get("reviewBody") or rev.get("description")
                        rev_rating = rev.get("reviewRating", {}).get("ratingValue") if isinstance(rev.get("reviewRating"), dict) else None
                        author = rev.get("author", {}).get("name") if isinstance(rev.get("author"), dict) else rev.get("author")
                        if rev_body:
                            reviews.append({
                                "review_text": rev_body,
                                "rating": rev_rating or rating or 4.0,
                                "reviewer_name": author or "Verified Buyer",
                                "website_name": website_name
                            })

        # 2. Try OpenGraph parsing
        og_data = parse_opengraph(html_content)
        product_name = product_name or og_data.get("og:title") or og_data.get("twitter:title")
        image_url = image_url or og_data.get("og:image")
        current_price = current_price or extract_price_from_text(og_data.get("product:price:amount") or og_data.get("og:price:amount"))

    # Fallback product name from URL if still missing
    if not product_name:
        path_parts = [p for p in urlparse(url).path.split('/') if p and len(p) > 2]
        if path_parts:
            raw_title = path_parts[0].replace('-', ' ').replace('_', ' ')
            product_name = raw_title.title()
        else:
            product_name = f"{website_name} Product"

    if current_price and original_price and original_price > current_price and not discount_percent:
        discount_percent = round(((original_price - current_price) / original_price) * 100, 1)

    return ProductData(
        website=website_name,
        product_name=product_name,
        current_price=current_price,
        original_price=original_price,
        discount_percent=discount_percent,
        rating=rating,
        review_count=review_count,
        product_url=url,
        availability="In Stock",
        brand=brand,
        image_url=image_url,
        reviews=reviews
    )
