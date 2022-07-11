from xml.etree.ElementTree import QName
import pandas as pd
import requests
from dotenv import load_dotenv
load_dotenv()
import os

# Retrieve Fremont bridge bike data from API pull and convert to dataframe
response = requests.get('https://data.seattle.gov/resource/65db-xm6k.json', headers={'X-App-Token': os.environ.get(
        'FREMONT_API_KEY')})

bridge_by_hour_df = pd.read_json(response.text)
bridge_by_hour_df = bridge_by_hour_df.drop(['fremont_bridge_sb', 'fremont_bridge_nb'], axis=1)
bridge_by_hour_df['date'] = pd.to_datetime(bridge_by_hour_df['date']).dt.date
bridge_df = bridge_by_hour_df.groupby('date').sum()
print(bridge_df)