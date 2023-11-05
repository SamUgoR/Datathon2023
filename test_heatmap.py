import numpy as np
import pandas as pd
import folium
from folium.plugins import HeatMap

# Load your data
data = pd.read_csv('merged_dataset_vbeta.csv')
# Replace 'N/R' values with 0 in the entire DataFrame
data.replace('N/R', 0, inplace=True)

# Convert all entries in 'Value' column to numeric, forcing non-numeric values to NaN and then replacing them with 0
data['Value'] = pd.to_numeric(data['Value'], errors='coerce').fillna(0)
data.columns = ['Organization', 'Category', 'Year', 'Value', 'Address', 'Coordinates']
data[['Latitude', 'Longitude']] = data['Coordinates'].str.split(',', expand=True).astype(float)

# Assuming you want to aggregate the values for each organization per year
summary = data.groupby(['Year', 'Latitude', 'Longitude', 'Organization'])['Value'].sum().reset_index()

# Create folium map object
m = folium.Map(location=[46.2044, 6.1432], zoom_start=13)  # Center of Geneva

# For each year, create a heatmap layer
for year in summary['Year'].unique():
    year_data = summary[summary['Year'] == year]
    heat_data = year_data[['Latitude', 'Longitude', 'Value']].values.tolist()
    
    # Add heatmap layer to the map for the specific year
    HeatMap(heat_data, radius=50, name=str(year)).add_to(m)

    # Add a circle marker for each organization in the year
    for _, row in year_data.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=5,  # Static radius for markers, you might want to scale this
            popup=f'Year: {year}<br>Organization: {row["Organization"]}<br>Emission in kg of CO2/year: {row["Value"]}',
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(m)

# Add Layer control to switch between years
folium.LayerControl().add_to(m)

# Save map to an HTML file
m.save('heatmap_original_points.html')
