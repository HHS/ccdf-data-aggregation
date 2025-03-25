import folium
import pandas as pd
import math

# Create a map centered on Massachusetts
ma_map = folium.Map(location=[42.407211, -71.382439], zoom_start=8)

# List of cities with their coordinates and zip codes
locations = [
    {"name": "Pittsfield", "zip": "01201", "lat": 42.4500, "lon": -73.2611}, 
    {"name": "Great Barrington", "zip": "01230", "lat": 42.1962, "lon": -73.3608}, 
    {"name": "Springfield", "zip": "01103", "lat": 42.1015, "lon": -72.5898}, 
    {"name": "Worcester", "zip": "01608", "lat": 42.2626, "lon": -71.8023}, 
    {"name": "Fitchburg", "zip": "01420", "lat": 42.5834, "lon": -71.8023}, 
    {"name": "Southbridge", "zip": "01550", "lat": 42.0751, "lon": -72.0334}, 
    {"name": "Boston", "zip": "02108", "lat": 42.3601, "lon": -71.0589},
    {"name": "Framingham", "zip": "01702", "lat": 42.2793, "lon": -71.4162}, 
    {"name": "Lowell", "zip": "01852", "lat": 42.6334, "lon": -71.3162}, 
    {"name": "Salem", "zip": "01970", "lat": 42.5195, "lon": -70.8967}, 
    {"name": "Gloucester", "zip": "01930", "lat": 42.6159, "lon": -70.6628}, 
    {"name": "Brockton", "zip": "02301", "lat": 42.0834, "lon": -71.0180}, 
    {"name": "New Bedford", "zip": "02740", "lat": 41.6362, "lon": -70.9342}, 
    {"name": "Hyannis", "zip": "02601", "lat": 41.6524, "lon": -70.2889}, 
    {"name": "Provincetown", "zip": "02657", "lat": 42.0584, "lon": -70.1787}, 
    {"name": "North Adams", "zip": "01247", "lat": 42.7000, "lon": -73.1088}, 
    {"name": "Greenfield", "zip": "01301", "lat": 42.5878, "lon": -72.5994},
    {"name": "Huntington", "zip": "01050", "lat": 42.2651, "lon": -72.8734}, 
    {"name": "Falmouth", "zip": "02540", "lat": 41.5526, "lon": -70.6163}, 
    {"name": "Chatham", "zip": "02633", "lat": 41.6818, "lon": -69.9598},
    {"name": "Nantucket", "zip": "02554", "lat": 41.2835, "lon": -70.0994}, 
    {"name": "Vineyard Haven", "zip": "02568", "lat": 41.4535, "lon": -70.6106}, 
    {"name": "Plymouth", "zip": "02360", "lat": 41.9584, "lon": -70.6673}, 
    {"name": "Attleboro", "zip": "02703", "lat": 41.9446, "lon": -71.2850},
    {"name": "Petersham", "zip": "01366", "lat": 42.4887, "lon": -72.1870}
]

# Define colors for better visibility
colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'darkblue', 
          'cadetblue', 'darkgreen', 'darkpurple', 'pink', 'lightorange', 'lightgreen', 'gray', 
          'black', 'beige', 'darkorange', 'lightgray', 'darkblue', 'cadetblue', 'pink']

# Convert 20 miles to meters (required by Folium)
radius_miles = 20
radius_meters = radius_miles * 1609.34  # 1 mile = 1609.34 meters

# Add each location and its radius circle to the map
for i, loc in enumerate(locations):
    # Add a marker for the city
    folium.Marker(
        location=[loc["lat"], loc["lon"]],
        popup=f"{loc['name']} ({loc['zip']})",
        tooltip=loc["name"],
        icon=folium.Icon(color=colors[i % len(colors)])
    ).add_to(ma_map)
    
    # Add a circle with 20-mile radius
    folium.Circle(
        location=[loc["lat"], loc["lon"]],
        radius=radius_meters,
        popup=f"{loc['name']} - 20 mile radius",
        color=colors[i % len(colors)],
        fill=True,
        fill_opacity=0.2
    ).add_to(ma_map)

# Save the map to an HTML file
ma_map.save("MA_coverage_map.html")

print("Map created and saved as 'MA_coverage_map.html'")