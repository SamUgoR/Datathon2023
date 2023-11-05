import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Load your primary dataset
df_primary = pd.read_csv('organized_table_data.csv')

# Load the dataset with addresses
df_addresses = pd.read_csv('Coordinate_file.csv')

# Normalize the organization names in both datasets
df_primary['Normalized_Name'] = df_primary['Organization'].str.lower().str.replace('[^\w\s]', '', regex=True)
df_addresses['Normalized_Name'] = df_addresses['Institution Name'].str.lower().str.replace('[^\w\s]', '', regex=True)

# Define a function to match names and return the most similar one
def get_best_match(name, choices, scorer, cutoff):
    matches = process.extractOne(name, choices, scorer=scorer)
    if matches and matches[1] >= cutoff:
        return matches[0]
    else:
        return None

# Apply fuzzy matching to get the best match for each organization
df_primary['Best_Match'] = df_primary['Normalized_Name'].apply(
    lambda x: get_best_match(x, df_addresses['Normalized_Name'].unique(), fuzz.WRatio, cutoff=80)
)

# Merge the datasets based on the best match
df_final = pd.merge(
    df_primary,
    df_addresses,
    left_on='Best_Match',
    right_on='Normalized_Name',
    how='left'
)

# Select the relevant columns (drop the helper columns used for matching)
df_final = df_final[['Organization', 'Category', 'Year', 'Value', 'Address', 'coordinates']]

# Save the merged dataset
df_final.to_csv('merged_dataset.csv', index=False)
