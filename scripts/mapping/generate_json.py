# convert csv of geo data into a geojson file encoding the same information

import json
import pandas as pd
from datetime import datetime
import numpy as np

meta = pd.read_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/mapping/new/complete.csv")

meta = meta.dropna(subset=['Coordinates', 'Date'])

meta['Date'] = [datetime.strptime(str(date), '%B %d, %Y') for date in meta['Date']]

meta = meta.sort_values(by=['Archive'])

def type_to_int(string):
	types = ['BAnQ', 'British Columbia Historical Newspapers','British Newspaper Archives','LOC Conundrum Social',\
			"LOC Conundrum Supper", "LOC Conundrum Tea", 'NYS Historical Newspapers or Fulton']
	return types.index(string)

def make_coord(coord, archive):
	coordinates = (coord[:-1])[1:].split(',')
	coordinates = [float(coord) for coord in coordinates]
	if (coordinates[0] > -10):
		if archive != 'British Newspaper Archives':
			return None
	if (coordinates[1] < 15):
		return None
	return coordinates

meta['Coordinates'] = meta.apply(lambda row: make_coord(row['Coordinates'],row['Archive']), axis=1)


meta = meta.dropna(subset=['Coordinates', 'Date'])


def make_json(row):
	coordinates = row['Coordinates']
	date = row['Date']
	
	host = str(row['Organization_Hosting'])


	# The conundrum event took place in [LOCATION], as advertised by [NEWSPAPER] on [DATE]. ([ARCHIVE])
	description = 'The conundrum event took place in <strong>' + str(row['Location']) +\
				  '</strong>, as advertised by <strong>' + row['Newspaper'] + '</strong> on <strong>' +row['Date'].strftime('%B %d, %Y')+\
				  '</strong>. ' + row['Archive'] + "."
	
	body = {
		"type": "Feature",
		"properties": {
			"Newspaper": str(row['Newspaper']),
			'Persons': str(row['Persons']),
			"Host": str(host),
			"Location": str(row['Location']),
			'Comments': str(row['Notes']),
			"Year": date.year,
			"Type": type_to_int(row['Archive']),
			'description': str(description)
		},
		"geometry":
		{
			"type":"Point",
			"coordinates": coordinates
		}
	}

	return body

jsons = []
for index,row in meta.iterrows():
	jsons.append(make_json(row))


final = {
  "type": "FeatureCollection",
  "features": jsons
  }


path = "/Users/ndrezn/OneDrive - McGill University/Github/nathaliecookehathi.github.io/data.geojson"
with open(path, 'w') as outfile:
	json.dump(final, outfile)