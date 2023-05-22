import requests
from bs4 import BeautifulSoup
import smtplib

# Email Settings
sender_email = input("Enter your email address: ")
sender_password = input("Enter your email password: ")
recipient_email = input("Enter recipient email address: ")

# Product URL on Amazon
product_url = input("Enter Amazon product URL: ")

#  Get the current price of the product
def get_product_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    price = soup.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[1:].replace(',', ''))
    return converted_price

# Compare the price and send the email if the price has decreased
def send_price_alert():
    current_price = get_product_price(product_url)

    if current_price < desired_price:
        message = f"Subject: Price Alert for {product_url}\n\nThe price of the product you are tracking has dropped below your desired price.\nCurrent Price: ${current_price}"
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, recipient_email, message)
        print("Price alert email sent successfully.")

# Request the desired price and periodically check the price of the product
desired_price = float(input("Enter your desired price: "))

while True:
    send_price_alert()
    interval = 3600  # Check every hour
    time.sleep(interval)