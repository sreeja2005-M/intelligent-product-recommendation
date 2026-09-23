from croma import scrape_croma


url = "https://www.croma.com/preethi-cocosta-coconut-scraper-citrus-juicer-black-/p/274212"

result = scrape_croma(url)

print("\n========== CROMA SCRAPER RESULT ==========")

for key, value in result.items():
    print(f"{key}: {value}")

print("==========================================")