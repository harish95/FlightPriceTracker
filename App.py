from flightInfo import FlightINFO
import yagmail
import time
from twilio.rest import Client
import os



# Flight API credentials
API_KEY = os.environ('FLIGHT_API_KEY')
API_SECRET = os.environ('FLIGHT_API_SEC')
token_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
flight_offers_url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'

# Gmail Credentials
sender = "datanewshub@gmail.com"
my_secret = os.environ('YA_MAIL_SECRET')
yag = yagmail.SMTP(user=sender, password=my_secret)


# Twilio Credentials
account_sid = os.environ('TW_SID')
auth_token = os.environ('TW_AUTH_TOKEN')
client = Client(account_sid, auth_token)




flight = FlightINFO(API_KEY=API_KEY,API_SECRET=API_SECRET,token_url=token_url,flight_offers_url=flight_offers_url)
flight.generate_token()



while True:
    flight.get_flight_data(origin='BOM', destination='DEL', date='2024-06-30')
    flight_data = flight.process_flights()

    if flight_data.iloc[0]['price'] <= 4000:

        subject = f"flight available from {flight_data.iloc[0]['source']} to {flight_data.iloc[0]['destination']} for Price : {flight_data.iloc[0]['price']}"
        contents = f"flight available from {flight_data.iloc[0]['source']} to {flight_data.iloc[0]['destination']} for Price : {flight_data.iloc[0]['price']} by {flight_data.iloc[0]['carrier']} on time: {flight_data.iloc[0]['departure']} sent by harish"

        # Sending Mail
        yag.send(to="dewific518@egela.com", subject=subject, contents=contents)
        print("Email Sent!")

        # Sending whatsapp message
        message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=contents,
        to='whatsapp:+917798125301')
        print(message.sid)

    time.sleep(60)



