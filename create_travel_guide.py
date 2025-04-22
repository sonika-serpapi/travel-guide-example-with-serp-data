from serpapi import GoogleSearch
import os, json
from dotenv import load_dotenv
load_dotenv()

# Load the API key from the environment variable
# Make sure to set the SERPAPI_API_KEY in your environment variables
# You can do this by creating a .env file with the following content:
# SERPAPI_API_KEY=your_api_key_here

api_key = os.environ["SERPAPI_API_KEY"]

def get_travel_results():

    # Define the location for which you want to create a travel guide
    # You can change this to any location you want
    location = "San Francisco, California"

    # Google Maps API request to get points of interest in the location
    params = {
        "api_key": api_key,
        "engine": "google_maps",
        "q": f'Points of Interest in {location}',
        "hl": "en",
        "gl": "us"
    }

    search = GoogleSearch(params)
    local_results = search.get_dict()["local_results"]

    sight_results = []
    for result in local_results:
        sight_details = {}
        sight_details["title"] = result["title"]
        sight_details["thumbnail"] = result["thumbnail"]
        sight_results.append(sight_details)

    # Google Local API request to get top restaurants in the location
    params = {
        "api_key": api_key,
        "engine": "google_local",
        "q": f'Best restaurants in {location}',
        "hl": "en",
        "gl": "us"
    }

    search = GoogleSearch(params)
    local_results = search.get_dict()["local_results"]

    restaurant_results = []

    for result in local_results:
        restaurant_details = {}
        restaurant_details["title"] = result["title"]
        restaurant_details["rating"] = result["rating"]
        restaurant_details["type"] = result["type"]
        restaurant_details["address"] = result["address"]
        restaurant_details["thumbnail"] = result["thumbnail"]
        restaurant_results.append(restaurant_details)


    # Google Hotels API request to get best hotels in the location
    params = {
        "api_key": api_key,
        "engine": "google_hotels",
        "q": f'Best Hotels in {location}',
        "hl": "en",
        "gl": "us",
        "check_in_date": "2025-12-12",
        "check_out_date": "2025-12-15",
        "currency": "USD",
        "hotel_class": "4,5"
    }

    search = GoogleSearch(params)
    properties = search.get_dict()["properties"]

    hotel_results = []

    for result in properties:
        hotel_details = {}
        hotel_details["name"] = result["name"]
        hotel_details["link"] = result["link"]
        hotel_details["rate_per_night"] = result["rate_per_night"]["lowest"]
        hotel_details["thumbnail"] = result["images"][0]["thumbnail"]
        hotel_details["rating"] = result["overall_rating"]
        hotel_results.append(hotel_details)

    # Writing the data to a markdown file
    with open("generated_sanfrancisco_guide.md", "w") as f:
        f.write("# San Francisco Travel Guide\n\n")
        f.write("## Top Sights\n")
        for sight in sight_results:
            f.write(f"### {sight["title"]}\n")
            f.write(f"![{sight["title"]}]({sight["thumbnail"]})\n\n")
            
        f.write("## Top Restaurants\n")
        for restaraunt in restaurant_results:
            f.write(f"### {restaraunt["title"]}\n")
            f.write(f"![{restaraunt["title"]}]({restaraunt["thumbnail"]})\n\n")
            f.write(f"#### Cuisine: {restaraunt["type"]}\n")
            f.write(f"#### Rating: {restaraunt["rating"]}/5\n")
            f.write(f"#### Address: {restaraunt["address"]}\n")
        
        f.write("## Top Hotels\n")
        for hotel in hotel_results:
            f.write(f"### {hotel["name"]}\n")
            f.write(f"![{hotel["name"]}]({hotel["thumbnail"]})\n\n")
            f.write(f"#### Link: {hotel["link"]}\n")
            f.write(f"#### Rate per night: {hotel["rate_per_night"]}\n")
            f.write(f"#### Rating: {hotel["rating"]}/5\n")

        print("Travel Guide Created Successfully!")
    return

get_travel_results()