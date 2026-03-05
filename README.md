# 🌾 Fasal Bazaar

**A hyper-local peer-to-peer marketplace connecting farmers directly with buyers — no middlemen, no long-haul logistics.**

Fasal Bazaar cuts out traditional agricultural middlemen by letting farmers list produce and buyers discover it within a **5–20 km radius**. Built for the Indian agricultural context, with real-time mandi price data, WhatsApp-based alerts, and full Hindi/English support.

---

## ✨ Features

- **Hyper-local discovery** — Postal Pincode API + Haversine distance search limits listings to a realistic pickup/delivery radius
- **Dual-role onboarding** — separate, purpose-built flows for buyers and sellers
- **Crop listings** — organized into 6 categories (Grains, Pulses, Vegetables, Fruits, Oilseeds, Spices & Fibers) with harvest images and metadata
- **Buyer Requests** — buyers post specific crop needs; farmers get notified of unmet local demand
- **Live Mandi price feed** — pulls real government market rates (Agmarknet/Data.gov.in) so farmers never sell blind
- **Price benchmarking & trends** — dynamic comparison against live rates, plus 7-day price trend charts
- **WhatsApp notifications** — instant alerts for buyer interest and matching requests, no need to babysit the app
- **Voice-first listing** — chat/voice-based crop listing for low digital-literacy users
- **Bilingual UI** — full Hindi/English toggle via Reverie API
- **Seller reviews & reputation** — trust scoring based on trade history

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python (Flask) |
| Database | PostgreSQL |
| Auth | JWT |
| Notifications | WhatsApp API |
| Localization | Reverie API |
| Market Data | Agmarknet / Data.gov.in Mandi API |

---

## 📁 Project Structure

```
backend/
├── server.py           # App entry point
├── db.py                # Database connection
├── middleware/
│   └── auth.py          # JWT auth middleware
└── routes/
    ├── auth.py           # Login/signup
    ├── listings.py        # Crop listings
    ├── requests.py         # Buyer requests
    ├── cart.py              # Cart handling
    ├── transactions.py       # Order/transaction logic
    ├── mandi.py                # Live price API integration
    ├── reviews.py                # Reputation system
    ├── translate.py                # Hindi/English localization
    ├── chat.py                      # Voice/chat listing backend
    └── utils.py

templates/
├── Homepage.html / .css / .js
├── buying.html / buying-script.js
├── selling.html / selling-script.js
├── Product_Page.html / .css / .js
├── Request_Page.html / .js
├── chat-listing.html / .js
├── voice-listing.html / .js
├── mandi.html
├── checkout.html
├── Crop photos/          # Listing images
└── schema.sql            # Database schema
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- PostgreSQL
- A `.env` file with your API keys (Mandi API, Reverie, WhatsApp, DB credentials — see `.env.example` if provided, or set up your own)

### Setup

```bash
# Clone the repo
git clone https://github.com/SARANGSSP/FasalBazaar.git
cd FasalBazaar

# Set up a virtual environment
python -m venv backend/venv
source backend/venv/Scripts/activate   # Windows (Git Bash)
# or: source backend/venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Set up the database
psql -U your_user -d your_db -f templates/schema.sql

# Run the server
python backend/server.py
```
---

## 📄 License

This project was built for academic purposes as part of a Bachelor of Technology curriculum at VIT Bhopal University.
