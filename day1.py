# Day 1 - Python Basics

# variable
rating = 4

# list 
tags = ["CLEANLINES", "SERVICE"]

# dictionary (JSON-like)
review = {
    "hotel_id": "HOTEL_001",
    "rating": rating,
    "text": "Rooms were clean but price was high"
}
 # function
def analyze_review(review_text):
    if "price" in review_text.lower():
        return "REJECT"
    else:
        return "PUBLISH"

decision = analyze_review(review["text"])

print("Decision:", decision)
print("Review:", review)
print("Tags:", tags)
        