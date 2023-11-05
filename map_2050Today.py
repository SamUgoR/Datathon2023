import numpy as np
import pandas as pd
import folium
from folium.plugins import HeatMap
from branca.colormap import LinearColormap

# Load your data
data = pd.read_csv('merged_dataset.csv')
# Replace 'N/R' values with 0 in the entire DataFrame
data.replace('N/R', 0, inplace=True)


# Convert all entries in 'Value' column to numeric, forcing non-numeric values to NaN and then replacing them with 0
data['Value'] = pd.to_numeric(data['Value'], errors='coerce').fillna(0)
data.columns = ['Organization', 'Category', 'Year', 'Value', 'Address', 'Coordinates']
data = data[data['Organization'].str.lower() != 'unige university of geneva']
data[['Latitude', 'Longitude']] = data['Coordinates'].str.split(',', expand=True).astype(float)

# Assuming you want to aggregate the values for each organization per year
summary = data.groupby(['Year', 'Latitude', 'Longitude', 'Organization'])['Value'].sum().reset_index()

# Create a color map
max_value = summary['Value'].max()
min_value = summary['Value'].min()
colormap = LinearColormap(colors=['blue', 'green', 'red'], vmin=min_value, vmax=max_value)
colormap.caption = 'Value Intensity'


# Create folium map object
m = folium.Map(location=[46.2044, 6.1432], zoom_start=13)  # Center of Geneva

# For each year, create a heatmap layer
for year in summary['Year'].unique():
    year_data = summary[summary['Year'] == year]
    heat_data = year_data[['Latitude', 'Longitude', 'Value']].values.tolist()
    # HeatMap(heat_data, radius=20, name=str(year)).add_to(m)

for _, row in year_data.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=5,
            popup=f'Year: {year}<br>Organization: {row["Organization"]}<br>Total emission in tC02/m2/year: {row["Value"]}',
            color=colormap(row['Value']),
            fill=True,
            fill_color=colormap(row['Value'])
        ).add_to(m)

# Add Layer control to switch between years
folium.LayerControl().add_to(m)


# Save map to an HTML file
m.save('heatmap_color_points.html')







# Add Layer control to switch between years
folium.LayerControl().add_to(m)

# Save map to an HTML file
m.save('map_2050Today.html')
