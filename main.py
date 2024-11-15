from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# URL to scrape
url = "https://appbrewery.github.io/instant_pot/"

# Headers for the request
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Dnt": "1",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
}

# Request page content
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Find the price and convert it to float
try:
    price = soup.find(class_="a-offscreen").get_text()
    price_without_currency = price.split("$")[1]
    price_as_float = float(price_without_currency)
    print(price_as_float)
except AttributeError:
    print("Failed to retrieve the price from the page.")
    price_as_float = None

# Get the product title
try:
    title = soup.find(id="productTitle").get_text().strip()
    print(title)
except AttributeError:
    print("Failed to retrieve the product title.")
    title = "Product"

# Set the price below which you would like to get a notification
BUY_PRICE = 100

# Check if the price meets the criteria and send email
if price_as_float and price_as_float < BUY_PRICE:
    message = f"{title} is on sale for {price}!"
    smtp_address = os.environ.get("SMTP_ADDRESS")
    email_address = os.environ.get("EMAIL_ADDRESS")
    email_password = os.environ.get("EMAIL_PASSWORD")

    # Ensure environment variables are loaded
    if smtp_address and email_address and email_password:
        try:
            with smtplib.SMTP(smtp_address, port=587) as connection:
                connection.starttls()  # Secure the connection
                connection.login(email_address, email_password)
                connection.sendmail(
                    from_addr=email_address,
                    to_addrs=email_address,
                    msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
                )
            print("Email sent successfully!")
        except smtplib.SMTPException as e:
            print(f"Failed to send email: {e}")
    else:
        print("Missing SMTP configuration. Please check your .env file.")
else:
    print("Price is above the target or could not be retrieved.")
