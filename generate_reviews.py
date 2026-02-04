import random
import json
import csv
from datetime import datetime
from pathlib import Path

# ---------- CONFIG ----------
HOTEL_ID = "HOTEL_001"
TOTAL_REVIEWS = 716

OUTPUT_JSONL = Path("data/reviews_raw.jsonl")
OUTPUT_CSV = Path("data/reviews_raw.csv")

# ---------- DATA POOLS ----------
REVIEWERS = [
    "Amit", "Rohit", "Sneha", "Pooja", "Rahul",
    "Ankit", "Neha", "Karan", "Simran", "Vikas"
]

SOURCES = ["google", "booking", "internal"]

POSITIVE_TEMPLATES = [
    "Great stay, very clean rooms and friendly staff",
    "Excellent hotel with nice location",
    "Amazing service and clean bathroom",
    "Loved the breakfast and the staff behavior",
    "Very nice hotel, will visit again"
]

NEGATIVE_TEMPLATES = [
    "Worst stay ever, very dirty rooms",
    "Bad experience, noisy at night",
    "Poor maintenance and rude staff",
    "Terrible hotel, bathroom was dirty",
    "Not good, rooms were smelly"
]

NEUTRAL_TEMPLATES = [
    "Hotel was okay, nothing special",
    "Average stay, decent location",
    "Rooms were fine but service was slow",
    "Okay experience, food was average",
    "Nothing great, nothing terrible"
]

PRICE_SNIPPETS = [
    "I paid 6000 per night",
    "Cost was ₹4500",
    "Price is too high for this hotel",
    "Tariff was 5000 INR",
]

PHONE_SNIPPETS = [
    "Call me at 9876543210",
    "My number is 9123456789",
]

EMAIL_SNIPPETS = [
    "Email me at test@gmail.com",
    "Contact: demo@yahoo.com",
]

LINK_SNIPPETS = [
    "Check www.fakehotel.com",
    "More details at http://spamlink.com",
]

# ---------- HELPER ----------
def random_date():
    return datetime.now().isoformat()

# ---------- GENERATION ----------
def generate_review(i: int) -> dict:
    sentiment_type = random.choice(["positive", "neutral", "negative"])

    if sentiment_type == "positive":
        text = random.choice(POSITIVE_TEMPLATES)
        rating = random.randint(4, 5)
    elif sentiment_type == "negative":
        text = random.choice(NEGATIVE_TEMPLATES)
        rating = random.randint(1, 2)
    else:
        text = random.choice(NEUTRAL_TEMPLATES)
        rating = 3

    # Inject problematic content randomly
    if random.random() < 0.3:
        text += ". " + random.choice(PRICE_SNIPPETS)
    if random.random() < 0.15:
        text += ". " + random.choice(PHONE_SNIPPETS)
    if random.random() < 0.1:
        text += ". " + random.choice(EMAIL_SNIPPETS)
    if random.random() < 0.1:
        text += ". " + random.choice(LINK_SNIPPETS)

    return {
        "review_id": f"R{i+1}",
        "hotel_id": HOTEL_ID,
        "reviewer_name": random.choice(REVIEWERS),
        "rating": rating,
        "review_text": text,
        "source": random.choice(SOURCES),
        "created_at": random_date()
    }

# ---------- MAIN ----------
def main():
    reviews = [generate_review(i) for i in range(TOTAL_REVIEWS)]

    OUTPUT_JSONL.parent.mkdir(exist_ok=True)
    OUTPUT_CSV.parent.mkdir(exist_ok=True)

    # Write JSONL
    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
        for r in reviews:
            f.write(json.dumps(r) + "\n")

    # Write CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = reviews[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reviews)

    print(f"Generated {len(reviews)} reviews")
    print(f"JSONL: {OUTPUT_JSONL}")
    print(f"CSV: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
