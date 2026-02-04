# ---------- IMPORTS ----------
import re
import json
import csv
from pathlib import Path
import mysql.connector
from fastapi import FastAPI

# ---------- APP ----------
app = FastAPI(title="Hotel Review Analysis POC")

# ---------- MYSQL CONFIG ----------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "heyimlearning12",
    "database": "review_poc"
}

# ---------- REGEX PATTERNS ----------
PRICE_REGEX = r"(₹|rs\.?|inr|\b\d{4,6}\b)"
PHONE_REGEX = r"\b\d{10}\b"
EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
LINK_REGEX = r"(http://|https://|www\.)"

# ---------- SIGNAL DETECTION ----------
def detect_signals(text: str) -> dict:
    text_lower = text.lower()
    return {
        "price": bool(re.search(PRICE_REGEX, text_lower)),
        "phone": bool(re.search(PHONE_REGEX, text_lower)),
        "email": bool(re.search(EMAIL_REGEX, text_lower)),
        "link": bool(re.search(LINK_REGEX, text_lower)),
    }

# ---------- SENTIMENT ----------
POSITIVE_WORDS = ["good", "great", "excellent", "nice", "amazing", "clean"]
NEGATIVE_WORDS = ["bad", "poor", "dirty", "worst", "terrible", "noisy"]

def detect_sentiment(text: str) -> str:
    text = text.lower()
    if any(w in text for w in POSITIVE_WORDS):
        return "SENTIMENT_POSITIVE"
    if any(w in text for w in NEGATIVE_WORDS):
        return "SENTIMENT_NEGATIVE"
    return "SENTIMENT_NEUTRAL"

# ---------- SUMMARY ----------
def generate_summary(text: str) -> str:
    return text[:80] + "..." if len(text) > 80 else text

# ---------- CORE ANALYSIS ----------
def analyze_review_logic(review: dict) -> dict:
    text = review["review_text"]

    signals = detect_signals(text)
    sentiment = detect_sentiment(text)
    summary = generate_summary(text)

    rejection_reasons = []
    if signals["price"]:
        rejection_reasons.append("PRICE_MENTIONED")
    if signals["phone"]:
        rejection_reasons.append("PHONE_NUMBER_MENTIONED")
    if signals["email"]:
        rejection_reasons.append("EMAIL_MENTIONED")
    if signals["link"]:
        rejection_reasons.append("LINK_MENTIONED")

    decision = "REJECT" if rejection_reasons else "PUBLISH"

    return {
        "review_id": review["review_id"],
        "hotel_id": review["hotel_id"],
        "rating": review["rating"],
        "publish_decision": decision,
        "rejection_reasons": json.dumps(rejection_reasons),
        "sentiment": sentiment,
        "summary": summary
    }

# ---------- MYSQL INSERT ----------
def insert_into_mysql(rows: list):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    query = """
    INSERT INTO reviews_enriched
    (review_id, hotel_id, rating, publish_decision, rejection_reasons, sentiment, summary)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    data = [
        (
            r["review_id"],
            r["hotel_id"],
            r["rating"],
            r["publish_decision"],
            r["rejection_reasons"],
            r["sentiment"],
            r["summary"]
        )
        for r in rows
    ]

    cursor.executemany(query, data)
    conn.commit()
    cursor.close()
    conn.close()

# ---------- HEALTH ----------
@app.get("/")
def health_check():
    return {"status": "ok"}

# ---------- SINGLE REVIEW ----------
@app.post("/reviews/analyze-one")
def analyze_one(review: dict):
    return analyze_review_logic(review)

# ---------- BULK ANALYSIS ----------
@app.post("/reviews/analyze-bulk")
def analyze_bulk():
    input_path = Path("data/reviews_raw.jsonl")
    output_path = Path("output/reviews_enriched.csv")

    results = []

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            review = json.loads(line)
            results.append(analyze_review_logic(review))

    insert_into_mysql(results)

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    return {
        "total_processed": len(results),
        "mysql_inserted": len(results),
        "csv_output": str(output_path)
    }

# ---------- SUMMARY REPORT ----------
@app.get("/reports/summary")
def summary_report():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total FROM reviews_enriched")
    total = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT publish_decision, COUNT(*) as count
        FROM reviews_enriched GROUP BY publish_decision
    """)
    publish_stats = cursor.fetchall()

    cursor.execute("""
        SELECT sentiment, COUNT(*) as count
        FROM reviews_enriched GROUP BY sentiment
    """)
    sentiment_stats = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "total_reviews": total,
        "publish_stats": publish_stats,
        "sentiment_stats": sentiment_stats
    }

  
      