import pandas as pd
import json

# Load your data
data = pd.read_csv('merged_dataset.csv')
# Load your data
data = pd.read_csv('merged_dataset.csv')
# Replace 'N/R' values with 0 in the entire DataFrame
data.replace('N/R', 0, inplace=True)


# Convert all entries in 'Value' column to numeric, forcing non-numeric values to NaN and then replacing them with 0
data['Value'] = pd.to_numeric(data['Value'], errors='coerce').fillna(0)
data.columns = ['Organization', 'Category', 'Year', 'Value', 'Address', 'Coordinates']
data[['Latitude', 'Longitude']] = data['Coordinates'].str.split(',', expand=True).astype(float)


# Function to convert DataFrame to GeoJSON
def df_to_geojson(df, properties, lat='Latitude', lon='Longitude'):
    geojson = {'type': 'FeatureCollection', 'features': []}
    for _, row in df.iterrows():
        feature = {'type': 'Feature',
                   'properties': {},
                   'geometry': {'type': 'Point',
                                'coordinates': []}}
        feature['geometry']['coordinates'] = [row[lon], row[lat]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson

# Define the properties you want to include
properties = ['Organization', 'Category', 'Year', 'Value', 'Address']
geojson_data = df_to_geojson(data, properties)

# Save to a file
with open('data.geojson', 'w') as f:
    json.dump(geojson_data, f)
