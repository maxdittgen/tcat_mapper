#clean up raw geotagged json
import json

# File path to the JSON file
file_path = "geotagged_ridership.json"

# Load the JSON file into a Python dictionary
with open(file_path, "r") as json_file:
    ridership = json.load(json_file)

print(len(ridership))
bad_stops = []
for stop in ridership.keys():
    if len(list(ridership[stop].keys())) < 4 or ridership[stop]['name'] == "Tompkins Consolidated Area Transit, Inc. (TCAT)":
        bad_stops.append(stop)

for stop in bad_stops:
    ridership.pop(stop)

print(len(ridership))

#save data as json
file_path = "clean_geotagged_ridership.json"

# Write the dictionary to a JSON file
with open(file_path, "w") as json_file:
    json.dump(ridership, json_file)