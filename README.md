Flight Price Tracker

This Python project tracks the prices of flights and sends alerts via email when the price falls below a specified threshold. The project is divided into two main files: App.py and flightInfo.py.

Requirements

1.	Python 3.7+
2.	Required Python packages:
o	requests
o	yagmail
o	beautifulsoup4
o	twilio
3.	Environment variables for sensitive information


Installation
1.	Clone the repository:
git clone <repository_url>
cd <repository_directory>

2.	Install the required Python packages:
pip install requests yagmail beautifulsoup4 twilio

3.	Set up environment variables:

o	YA_MAIL_SECRET: Yagmail password for the sender email account.
o	TW_SID: Twilio Account SID.
o	TW_AUTH_TOKEN: Twilio Auth Token.

These can be set in your operating system or within a .env file.

Configuration

1.	Gmail Credentials: Set the sender email and obtain the Yagmail password from the environment variables:
sender = "youremail@gmail.com"
my_secret = os.environ['YA_MAIL_SECRET']
yag = yagmail.SMTP(user=sender, password=my_secret)

2.	Twilio Credentials: Set the Twilio credentials from the environment variables:
account_sid = os.environ['TW_SID']
auth_token = os.environ['TW_AUTH_TOKEN']
client = Client(account_sid, auth_token)

3.	Flight URL and Price Threshold: Modify the URL and price_threshold in App.py according to your needs:
URL = "https://www.exampleflightwebsite.com/flight-details"
price_threshold = 5000

Usage

Run the script:
python App.py

The script will:
1.	Fetch flight information from the specified URL.
2.	Parse the flight details and price.
3.	Check if the price is below the specified threshold.
4.	Send an email and/or WhatsApp message if the price condition is met.
5.	Wait for a specified interval and repeat the process.

Code Overview

App.py

This is the main script that runs the flight price tracker.

import time
import yagmail
import os
from twilio.rest import Client
from flightInfo import get_flight_info

# Gmail Credentials
sender = "youremail@gmail.com"
my_secret = os.environ['YA_MAIL_SECRET']
yag = yagmail.SMTP(user=sender, password=my_secret)

# Twilio Credentials
account_sid = os.environ['TW_SID']
auth_token = os.environ['TW_AUTH_TOKEN']
client = Client(account_sid, auth_token)

URL = "https://www.exampleflightwebsite.com/flight-details"
price_threshold = 5000

while True:
    flight_name, price = get_flight_info(URL)
    if price <= price_threshold:
        subject = f"Alert!!! Price of {flight_name} is now {price}"
        contents = f"Alert!!! Price of {flight_name} is now {price}"

        # Sending Email
        yag.send(to="recipientemail@example.com", subject=subject, contents=contents)
        print("Email Sent!")

        # Sending WhatsApp message
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=contents,
            to='whatsapp:+yourwhatsappnumber'
        )

    time.sleep(3600)  # Check every hour


flightInfo.py

This script contains the function to fetch and parse flight information.

import requests
from bs4 import BeautifulSoup

def get_flight_info(URL):
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    flight_name = soup.find("div", {"class": "flight-name"}).text
    price = int(soup.find("span", {"class": "flight-price"}).text.replace(',', '').replace('₹', ''))

    return flight_name, price

Notes
•	Ensure that the URL provided in App.py is correct and accessible.
•	Make sure the environment variables are set correctly to avoid runtime errors.
•	Adjust the URL and price threshold as needed.
