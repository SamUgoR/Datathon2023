import pandas as pd

# Load your data
data = pd.read_csv('merged_dataset_vbeta.csv')

# Replace 'N/R' values with NaN and then fill with 0
data.replace('N/R', pd.NA, inplace=True)
data.fillna(0, inplace=True)
data.columns = ['Organization', 'Category', 'Year', 'Value', 'Address', 'Coordinates']

# Convert all entries in 'Value' column to numeric, forcing non-numeric values to NaN and then replacing them with 0
data['Value'] = pd.to_numeric(data['Value'], errors='coerce').fillna(0)

# Assuming 'Coordinates' column is in the format 'Latitude,Longitude'
# Split 'Coordinates' into two new columns 'Latitude' and 'Longitude'
data[['Latitude', 'Longitude']] = data['Coordinates'].str.split(',', expand=True)

# Convert the new 'Latitude' and 'Longitude' columns to numeric
data['Latitude'] = pd.to_numeric(data['Latitude'], errors='coerce').fillna(0)
data['Longitude'] = pd.to_numeric(data['Longitude'], errors='coerce').fillna(0)

# Remove the original 'Coordinates' column as it's no longer needed
data.drop(columns=['Coordinates'], inplace=True)

# Ensure categorical data is in string format
data['Organization'] = data['Organization'].astype(str)
data['Category'] = data['Category'].astype(str)
data['Year'] = data['Year'].astype(str)

# Save the cleaned data to a new CSV file
data.to_csv('cleaned_dataset_for_qgis.csv', index=False)

print("CSV file has been cleaned and prepared for QGIS.")
