import csv
import requests
import json

ridership = {}

# Function to parse the stop name
def parse_stop(stop):
    return stop.split('-', 1)[1].strip()

# parse the ridership dict to get google maps coordinates
def getCoords(query):
    # Define the payload
    payload = {
        "textQuery": query
    }

    # Define the headers
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": "AIzaSyB3r9vVcO3nTJTUE2bv8Zc7wShNa5bo2Cw",
        "X-Goog-FieldMask": "places.displayName,places.location"
    }

    # Define the API endpoint
    url = "https://places.googleapis.com/v1/places:searchText"

    # Send the POST request
    response = requests.post(url, json=payload, headers=headers).json()

    # Print the response
    loc = response["places"][0]['location']
    return (response["places"][0]['displayName']['text'],(loc['latitude'],loc['longitude']))

# Read the CSV file
with open('ridership.csv', newline='', encoding='utf-8') as csvfile:
    # Skip the BOM by using a BOM_UTF8 codec
    csvfile.seek(0)
    if csvfile.read(3) != '\xef\xbb\xbf':
        csvfile.seek(0)
    reader = csv.DictReader(csvfile, delimiter=',')
    
    # Get the corrected fieldnames (removing BOM)
    fieldnames = [fieldname.strip('\ufeff') for fieldname in reader.fieldnames]
    
    # Use the corrected fieldnames
    reader = csv.DictReader(csvfile, delimiter=',', fieldnames=fieldnames)
    next(reader)  # Skip the header row

    print(reader.fieldnames)
    count = 0
    for row in reader:
        count += 1
        if count > 600:
            break
        try:
            stop = parse_stop(row['Stop'])
        except:
            continue
        boards = int(row['APC Boards'].replace(',', ''))
        alights = int(row['APC Alights'].replace(',', ''))
        ridership[stop] = {'boards': boards, 'alights': alights}

count = 0
for stop in list(ridership.keys()):
    count += 1
    try:
        query = stop + " TCAT bus stop Ithaca NY"
        print("tagging stop " + str(count) + " out of 600...")
        (displayName, coords) = getCoords(query)
        ridership[stop]["coords"] = coords
        ridership[stop]["name"] = displayName
    except:
        print("ERROR: could not locate " + str(stop))



#save data as json
file_path = "geotagged_ridership.json"

# Write the dictionary to a JSON file
with open(file_path, "w") as json_file:
    json.dump(ridership, json_file)