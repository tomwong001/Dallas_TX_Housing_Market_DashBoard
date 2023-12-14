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


# Define the latitude and longitude bounds
lat_bounds = (32.2, 33.1)
long_bounds = (-97.2, -96.2)

# Define colors for each dataset
colors = {
    'zillow_scrap_cleaned': 'black',
    'City_Historical_Attractions_Cle': 'blue',
    'Cleaned - Dallas Offense Incide': 'red'
}

# Correct the latitude and longitude column names
lat_long_columns_corrected = {
    'zillow_scrap_cleaned': ('Latitude', 'Longitude'),
    'City_Historical_Attractions_Cle': ('Latitude', 'Longitude'),
    'Cleaned - Dallas Offense Incide': ('geocoded_column/latitude', 'geocoded_column/longitude')
}

# Define label names for each dataset
labels = {
    'zillow_scrap_cleaned': 'Houses',
    'City_Historical_Attractions_Cle': 'Historical Attractions',
    'Cleaned - Dallas Offense Incide': 'Offense Incidents'
}


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


# Create a new plot
plt.figure(figsize=(10, 10))

# Iterate over datasets and plot the filtered locations
for sheet, (lat_col, long_col) in lat_long_columns_corrected.items():
    # Filter data based on latitude and longitude bounds
    filtered_data = datasets[sheet][
        (datasets[sheet][lat_col].between(*lat_bounds)) &
        (datasets[sheet][long_col].between(*long_bounds))
        ]

    # Check if the dataset is zillow_scrap_cleaned and adjust the marker style and size
    if sheet == 'zillow_scrap_cleaned':
        plt.scatter(filtered_data[long_col], filtered_data[lat_col], color=colors[sheet], label=labels[sheet],
                    alpha=0.8, s=100, edgecolor='k', marker='D')
    else:
        plt.scatter(filtered_data[long_col], filtered_data[lat_col], color=colors[sheet], label=labels[sheet],
                    alpha=0.5)

# Set plot labels and legend
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Locations Visualization on Map')
plt.legend()

# Show the plot
plt.show()






