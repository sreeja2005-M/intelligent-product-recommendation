from playwright.sync_api import sync_playwright


def scrape_flipkart_reviews(url):

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("Opening Flipkart product page...")

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(3000)

        print("\n========== FLIPKART REVIEWS ==========")

        verified_buyers = page.get_by_text(
            "Verified Buyer",
            exact=True
        )

        reviews = []

        for i in range(verified_buyers.count()):

            element = verified_buyers.nth(i)
            container = element

            for level in range(1, 7):

                container = container.locator("..")

                try:
                    text = container.inner_text().strip()
                except:
                    continue

                lines = [
                    line.strip()
                    for line in text.splitlines()
                    if line.strip()
                ]

                has_rating = any(
                    line in ["1", "2", "3", "4", "5"]
                    for line in lines
                )

                has_verified = "Verified Buyer" in lines

                if has_rating and has_verified and len(lines) >= 5:

                    # Remove duplicate containers
                    if text in [
                        review["raw_text"]
                        for review in reviews
                    ]:
                        break

                    rating = None
                    review_title = None
                    review_date = None
                    review_text = None
                    reviewer_name = None

                    # Rating
                    for line in lines:
                        if line in ["1", "2", "3", "4", "5"]:
                            rating = int(line)
                            break

                    # Review title
                    titles = [
                        "Awesome",
                        "Delightful",
                        "Good choice",
                        "Classy product",
                        "Worth the money",
                        "Fabulous!",
                        "Perfect product!"
                    ]

                    for line in lines:
                        if line in titles:
                            review_title = line
                            break

                    # Date
                    for line in lines:
                        if "years ago" in line or "year ago" in line:
                            review_date = line
                            break

                    # Reviewer name
                    verified_index = lines.index(
                        "Verified Buyer"
                    )

                    if verified_index > 0:
                        reviewer_name = lines[
                            verified_index - 1
                        ]

                    # Review text
                    if review_title and review_date:

                        title_index = lines.index(
                            review_title
                        )

                        date_index = lines.index(
                            review_date
                        )

                        # Usually:
                        # Rating
                        # Title
                        # Date
                        # Review text

                        if date_index + 1 < len(lines):

                            review_text = lines[
                                date_index + 1
                            ]

                    reviews.append({
                        "rating": rating,
                        "review_title": review_title,
                        "review_date": review_date,
                        "reviewer_name": reviewer_name,
                        "review_text": review_text,
                        "website_name": "Flipkart",
                        "raw_text": text
                    })

                    break

        # Display structured reviews

        for index, review in enumerate(
            reviews,
            start=1
        ):

            print(f"\nReview {index}")
            print("Rating:", review["rating"])
            print("Title:", review["review_title"])
            print("Date:", review["review_date"])
            print("Reviewer:", review["reviewer_name"])
            print("Review:", review["review_text"])
            print("Website:", review["website_name"])

        print(
            "\nTotal structured reviews:",
            len(reviews)
        )

        print("======================================")

        browser.close()

        return reviews


if __name__ == "__main__":

    url = input(
        "Enter Flipkart product URL: "
    ).strip()

    if not url.startswith(
        ("http://", "https://")
    ):
        url = "https://" + url

    scrape_flipkart_reviews(url)