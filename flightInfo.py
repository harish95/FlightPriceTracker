import requests
import json
import os
import pandas as pd
import numpy as np

class FlightINFO():
    def __init__(self,API_KEY,API_SECRET,token_url,flight_offers_url):
        # Your Amadeus API credentials
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        
        # Endpoint to get the access token
        self.token_url = token_url
        self.flight_offers_url = flight_offers_url

        # Data to be sent for getting the token
        self.data = {
        'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': API_SECRET
        }

    def generate_token(self):
        # Make the request to get the access token
        self.response = requests.post(self.token_url, data=self.data)

        # Parse the response to get the token
        token_response = self.response.json()
        self.access_token = token_response['access_token']

        print("Token Generated")
        return self.access_token

    def get_flight_data(self,origin,destination,date,adults=1,currency='INR',nonStop='true'):
        headers = {'Authorization': f'Bearer {self.access_token}'}

        params = {
        'originLocationCode': origin,
        'destinationLocationCode': destination,
        'departureDate': date,
        'adults': adults,
        'currencyCode': currency,
        'nonStop': nonStop
        }

        # add returnDate parameter for return flights

        response = requests.get(url=self.flight_offers_url, headers=headers, params=params)

        self.result = response.json()
        
        print("flights Fetched")
        return self.result
    
    def process_flights(self):
        flight_data = self.result['data']
        flights = []

        for flight in flight_data:
    
            flight_info =  [flight['id'],
                        flight['itineraries'][0]['segments'][0]['departure']['iataCode'],
                       flight['itineraries'][0]['segments'][0]['arrival']['iataCode'],
                       flight['itineraries'][0]['segments'][0]['departure']['at'],
                       flight['itineraries'][0]['segments'][0]['arrival']['at'],
                       flight['itineraries'][0]['segments'][0]['carrierCode'],
                        flight['price']['total']]
            flights.append(flight_info)

        flight_data = pd.DataFrame(np.array(flights),columns=['id','source','destination','departure','arrival','carrier','price'])
        flight_data['price'] = flight_data['price'].astype(float)
        self.cheapest_flights = flight_data.sort_values(by=['price'],ascending=True).head(3)
        
        print("Flights processed")
        return self.cheapest_flights
    
    
    
    

        
    