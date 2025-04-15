#!/bin/bash
set -e

echo " Starting web scraper application..."

echo " Initializing scraper for URL: ${SCRAPE_URL}"
cd /app
node scraper/scrape.js

echo " Starting Flask server..."
/app/venv/bin/python3 server/app.py
