import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load each sheet from the Excel file
xls = pd.ExcelFile('Python Data .xlsx')

# Get the names of all sheets in the Excel file
sheet_names = xls.sheet_names

# Load and display a snippet of each dataset to identify the latitude and longitude columns
datasets = {}

for sheet in sheet_names:
    # Skip the FEMA dataset
    if "FEMA" in sheet:
        continue

    # Load and display a snippet of each sheet
    datasets[sheet] = xls.parse(sheet)


'''User input'''
# Initialize filter parameters
price_range = (300000, 1000000)
beds = 2
baths = 2
# Filter the zillow_scrap_cleaned dataset
datasets['zillow_scrap_cleaned'] = datasets['zillow_scrap_cleaned'][
    (datasets['zillow_scrap_cleaned']['Price'].between(*price_range)) &
    (datasets['zillow_scrap_cleaned']['Beds'] == beds) &
    (datasets['zillow_scrap_cleaned']['Bathrooms'] == baths)
]


# Define the function to calculate distance between two coordinates (latitude, longitude)
def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance in meters between two points on the earth."""
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    r = 6371  # Radius of Earth in kilometers
    return c * r * 1000  # Convert to meters

# Get the coordinates of houses and offense incidents
houses = datasets['zillow_scrap_cleaned'][['Latitude', 'Longitude']]
incidents = datasets['Cleaned - Dallas Offense Incide'][['geocoded_column/latitude', 'geocoded_column/longitude']]

# Calculate distance matrix
dist_matrix = np.array([[haversine(lat1, lon1, lat2, lon2) for lat2, lon2 in zip(incidents['geocoded_column/latitude'], incidents['geocoded_column/longitude'])] for lat1, lon1 in zip(houses['Latitude'], houses['Longitude'])])

# Count number of incidents within 500 meters of each house
incident_counts = np.sum(dist_matrix <= 500, axis=1)

# Count the number of houses with each incident count
house_counts = np.bincount(incident_counts)

# Generate x values from 0 to max number of incidents
x_values = np.arange(len(house_counts))

# Plot the bar chart
plt.figure(figsize=(10, 6))
plt.bar(x_values, house_counts, color='c', alpha=0.7)
plt.xlabel('Number of Offense Incidents Within 500m')
plt.ylabel('Number of Houses')
plt.title('Number of Houses vs Number of Nearby Offense Incidents')
plt.show()
