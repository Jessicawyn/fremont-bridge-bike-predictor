from xml.etree.ElementTree import QName
from numpy import concatenate
import pandas as pd
import requests
from dotenv import load_dotenv
load_dotenv()
import os
import datetime as dt
import time


# Retrieve Fremont bridge bike data from API pull and convert to dataframe
response = requests.get('https://data.seattle.gov/resource/65db-xm6k.json', headers={'X-App-Token': os.environ.get('FREMONT_API_KEY')})

bridge_by_hour_df = pd.read_json(response.text)
bridge_by_hour_df = bridge_by_hour_df.drop(['fremont_bridge_sb', 'fremont_bridge_nb'], axis=1)
bridge_by_hour_df['date'] = pd.to_datetime(bridge_by_hour_df['date']).dt.date
bridge_df = bridge_by_hour_df.groupby('date').sum().reset_index()
print(bridge_df)

# Retrieve historical daily temperatures & add to dataframe

def get_epoch_time(input_date):
        str_date = str(input_date).replace('date              ', '')
        year = int(str_date[0:4])
        month = int(str_date[5:7])
        day = int(str_date[8:10])
        return int(dt.datetime(year, month, day, 14, 0, 0).timestamp())

def get_historical_weather_data(epoch_time):
    latitude = 47.64774 
    long = -122.34980
    start_time = epoch_time
    historical_response = requests.get('https://api.openweathermap.org/data/3.0/onecall/timemachine', 
        params={'lat': latitude,
                'lon': long,
                'dt': start_time,
                'units': 'imperial',
                'appid': os.environ.get('OPEN_WEATHER_API_KEY')})
    response_json = historical_response.json()
    temperature = response_json['data'][0]['temp']
    time.sleep(2)  # Preventing throttling of free API
    return temperature

bridge_df['temperature_f'] = bridge_df.apply(lambda row: get_historical_weather_data(get_epoch_time(row)), axis=1)
print(bridge_df)


# TODO: Run simple linear regression in Numpy

# TODO: Use forecast API to allow user to enter date and retrieve forecasted temp
#       Return predicted number of bicycles crossing bridge based on forecast temp

# TODO: Create command prompt user interface to interact with program
#       Option 1: Load historical data & run linear regression
#       Option 2: Enter date to get forecast and return num of bike crossings based on regression
#       Option 3: Enter temperature and return num of bike crossings based on regression
#       Option 4: Exit