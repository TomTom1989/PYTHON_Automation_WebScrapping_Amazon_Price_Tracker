A Python script to track product prices from Amazon webpage and send email notifications if the price drops below a set threshold.

Features:
1) Web Scraping:
Scrapes product data (title and price) from the provided webpage using BeautifulSoup.
Extracts and processes the price to check if it meets a predefined target.

2) Price Alert:
Compares the current price with a user-defined target price (BUY_PRICE).
If the price is below the target, sends an email alert with the product details.

3) Email Notification:
Sends an email using SMTP if the product meets the criteria.
Email settings (SMTP address, email, and password) are securely loaded from an .env file using dotenv.
