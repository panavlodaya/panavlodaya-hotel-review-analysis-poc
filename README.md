# Hotel Review Analysis POC

## Overview
This project is a backend Proof of Concept for hotel review moderation and tagging.

It simulates how real hotel reviews are:
- Generated
- Analyzed
- Moderated
- Stored
- Reported

## Tech Stack
- Python
- FastAPI
- MySQL
- Regex-based business rules
- Swagger (OpenAPI)

## Features
- Generate realistic hotel reviews using AI
- Detect price, phone, email, and spam
- Decide publish vs reject
- Sentiment detection
- Store analyzed reviews in MySQL
- Export results to CSV
- Summary report API

## How to Run
```bash
pip install fastapi uvicorn mysql-connector-python
python -m uvicorn main:app --reload


- Supports bulk analysis from JSON, CSV, and JSONL files
- Stores analyzed reviews in MySQL
- Provides summary statistics via /reports/summary API
