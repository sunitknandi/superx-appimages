import requests
import json
import pandas as pd
import urllib
from mongoConnection import MongoDB


# Fetch Pollution data of various Indian Cities from below url
r = requests.get('https://api.openaq.org/v1/latest?country=IN&limit=10000')

# convert the desired data in dictionary format
air_data = json.loads(r.text)
air_data = air_data['results']

# Converting nested data into linear structure
air_list = []
for data in air_data:
    for measurement in data['measurements']:
        air_dict = {}
        air_dict['location'] = data['location']
        air_dict['city'] = data['city']
        air_dict['country'] = data['country']
        air_dict['parameter'] = measurement['parameter']
        air_dict['value'] = measurement['value']
        air_dict['lastUpdated'] = measurement['lastUpdated']
        air_dict['unit'] = measurement['unit']
        air_dict['sourceName'] = measurement['sourceName']
        air_list.append(air_dict)
print('len', len(air_list))

# Convert list of dict into pandas df
df = pd.DataFrame(air_list, columns=air_dict.keys())
print(df.size)

# connection to mongo db
mongoDB_obj = MongoDB(urllib.quote_plus('root'), urllib.quote_plus('poln@recover'), '104.155.187.175', 'Pollution_Data')
# Insert Data into MongoDB
mongoDB_obj.insert_into_db(df, 'Air_Quality_India')
