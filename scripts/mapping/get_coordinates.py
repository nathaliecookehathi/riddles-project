# gets the latitude and longitude of the locations of the suppers and attaches it to the existing dataframe

import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep
from geopy.exc import GeocoderTimedOut
from progress.bar import Bar


def get_loc(place):
    try:
        location = geolocator.geocode(place)
        
        if location is None:
            return None

        coord = (location.latitude, location.longitude)
        
        return coord
    except:
        return get_loc(place)


meta = pd.read_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/new/Conundrum_Social_CSV.csv")

meta = meta.dropna(how='all')
meta=meta.dropna(axis=1,how='all')

# countries = meta['Country']
# states = meta['State/Province']
# cities = meta['City']

# coords = []

# places = []
# for city,state,country in zip(cities,states,countries):
#     place = str(country)+ " " +str(state)+ " " + str(city)
#     places.append(place)

places = meta['Publisher']

meta['Coordinates'] = places

geolocator = Nominatim(user_agent='ndrezn')

print("Doing the thing.")

meta['Coordinates'] = meta['Coordinates'].apply(get_loc)

print("Coordinates collected.")

meta.to_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/new/conundrum_social_with_coordinates.csv")

