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

# testing_df = bridge_df['fremont_bridge'].nlargest(n=3)
# bridge_df['datehello'] = get_date(bridge_df['date'])

# Retrieve historical daily temperatures (coordinates of Fremont Bridge)

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
    print(temperature)
    time.sleep(2)
    return temperature



bridge_df['temperature'] = bridge_df.apply(lambda row: get_historical_weather_data(get_epoch_time(row)), axis=1)
print(bridge_df)
print(bridge_df.columns)
# 1651266000.0
# 1652648400.0


# latitude = 47.64774 
# long = -122.34980
# start_time =  get_epoch_time('date              2022-05-31jl')
# print(start_time)
# historical_response = requests.get('https://api.openweathermap.org/data/3.0/onecall/timemachine', 
#         params={'lat': latitude,
#                 'lon': long,
#                 'dt': start_time,
#                 'units': 'imperial',
#                 'appid': os.environ.get('OPEN_WEATHER_API_KEY')})
# response_json = historical_response.json()
# temperature = response_json['data'][0]['temp']


# print(historical_response.json())
# print(response_json)
# print(temperature)



# print(bridge_df.assign(temp=lambda x: datetime(x.date.year, x.date.month, x.date.day, 14, 0, 0)))
# testing_df = testing_df.assign(temp=lambda d: datetime(d.year, d.month, d.day, 14, 0, 0))
# print(testing_df)


# print(testing_df)
# print(historical_response.json())


# print(historical_response.url)