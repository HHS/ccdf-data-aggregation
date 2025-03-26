import folium
import pandas as pd
import math

# Create a map centered on New Hampshire
nh_map = folium.Map(location=[43.7, -71.5], zoom_start=8)

# List of cities with their coordinates and zip codes for New Hampshire
locations = [
    {"name": "Concord", "zip": "03301", "lat": 43.2081, "lon": -71.5376},
    {"name": "Berlin", "zip": "03570", "lat": 44.4695, "lon": -71.1851},
    {"name": "Lisbon", "zip": "03585", "lat": 44.2156, "lon": -71.9106},  
    {"name": "Rochester", "zip": "03867", "lat": 43.3044, "lon": -70.9761},
    {"name": "Keene", "zip": "03431", "lat": 42.9337, "lon": -72.2779},
    {"name": "Pittsburg", "zip": "03592", "lat": 45.0513, "lon": -71.3989}
]

# Define colors for better visibility
colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred']

# Convert 50 miles to meters (required by Folium)
radius_miles = 50
radius_meters = radius_miles * 1609.34  # 1 mile = 1609.34 meters

# Add each location and its radius circle to the map
for i, loc in enumerate(locations):
    # Add a marker for the city
    folium.Marker(
        location=[loc["lat"], loc["lon"]],
        popup=f"{loc['name']} ({loc['zip']})",
        tooltip=loc["name"],
        icon=folium.Icon(color=colors[i % len(colors)])
    ).add_to(nh_map)
    
    # Add a circle with 50-mile radius
    folium.Circle(
        location=[loc["lat"], loc["lon"]],
        radius=radius_meters,
        popup=f"{loc['name']} - 50 mile radius",
        color=colors[i % len(colors)],
        fill=True,
        fill_opacity=0.2
    ).add_to(nh_map)

# Save the map to an HTML file
nh_map.save("NH_coverage_map.html")

print("Map created and saved as 'NH_coverage_map.html'")