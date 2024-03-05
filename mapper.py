import folium
import json
from folium import plugins
from branca.colormap import LinearColormap, linear

ITHACA_COORDS = [42.4440, -76.5019]

# Create a map centered at the coordinates of the city
city_map = folium.Map(location=ITHACA_COORDS, zoom_start=12)

# Add markers from geotagged ridership
file_path = "clean_geotagged_ridership.json"
with open(file_path, "r") as json_file:
    ridership = json.load(json_file)

# create sliding color scale
colormap_b = linear.YlGnBu_09.scale(0, 2000) #boarding
colormap_a = linear.YlGnBu_09.scale(0, 2000) #alighting
# colormap_b = LinearColormap(colors= [(0,0,255),(128,0,128), (255,0,0)],vmin=0, vmax=20000) #boarding
# colormap_a = LinearColormap(colors= [(0,0,255),(128,0,128), (255,0,0)],vmin=0, vmax=20000) #alighting

#Add points to the map with colors based on the assigned values
for stop in list(ridership.keys()):
    loc = ridership[stop]["coords"]
    boards = ridership[stop]['boards']
    color_b = colormap_b(boards)
    alights = ridership[stop]['alights']
    color_a = colormap_a(alights)
    name = ridership[stop]['name']
    folium.CircleMarker(location=[loc[0], loc[1]], radius=5,
                        popup= name + ": " + str(alights) + " passengers alighted",
                        color=color_b, fill=True, fill_color=color_a).add_to(city_map)
    # folium.CircleMarker(location=[loc[0], loc[1]], radius=5,
    #                     color='blue' if point['value'] < threshold else 'red',
    #                     fill=True, fill_color='blue' if point['value'] < threshold else 'red').add_to(city_map)

city_map.add_child(colormap_a)

# Save the map as an HTML file
city_map.save("tcat_alight.html")