import requests

from database.places_dao import PlacesDAO
from database.routes_dao import RoutesDAO

text_query = "Libraries in Rome, Italy"
page_size = 10


class GoogleMaps:
    def __init__(self, api_key):
        self.api_key = "AIzaSyCGygp0SRJldfPq7nWt7kPNtaJ168VZH7E"

    def search_text(self, text_query, page_size, nextPageToken):
        url = "https://places.googleapis.com/v1/places:searchText"

        # Request headers
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": "*"
        }

        # Request body
        if nextPageToken:
            data = {
                "textQuery": text_query,
                "pageSize": page_size,
                "pageToken": nextPageToken
            }
        else:
            data = {
                "textQuery": text_query,
                "pageSize": page_size
            }

        try:
            # Send POST request
            response = requests.post(url, headers=headers, json=data)

            # Check if request was successful
            if response.status_code == 200:
                if "places" in response.json():
                    PlacesDAO().create_place(response.json()['places'])
                else:
                    print("There is no list of places")
                    return

                print("Success:", response.status_code)
                if "nextPageToken" in response.json():
                    self.search_text(text_query, page_size, response.json()['nextPageToken'])
                else:
                    print("There is no next page")
            else:
                print("Error:", response.status_code, response.text)
        except Exception as e:
            print("Error:", e)


class GoogleMaps:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_distance_time(self, origin_lat, origin_lng, dest_lat, dest_lng, travel_mode):
        if origin_lat == dest_lat and origin_lng == dest_lng:
            return None, None, None
        url = "https://routes.googleapis.com/directions/v2:computeRoutes"

        # Request headers
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"
        }

        # Request body
        data = {
            "origin": {
                "location": {
                    "latLng": {
                        "latitude": origin_lat,
                        "longitude": origin_lng
                    }
                }
            },
            "destination": {
                "location": {
                    "latLng": {
                        "latitude": dest_lat,
                        "longitude": dest_lng
                    }
                }
            },
            "travelMode": travel_mode,
            "languageCode": "en-US",
            "units": "IMPERIAL"
        }

        try:
            # Send POST request
            response = requests.post(url, headers=headers, json=data)

            # Check if request was successful
            if response.status_code == 200:
                result = response.json()
                if "routes" in result and len(result["routes"]) > 0:
                    route = result["routes"][0]
                    distance = route["distanceMeters"]
                    duration = route["duration"]
                    polyline = route["polyline"]["encodedPolyline"]
                    return distance, duration, polyline
                else:
                    print("No routes found.")
                    return None, None, None
            else:
                print("Error:", response.status_code, response.text)
                return None, None, None
        except Exception as e:
            print("Error:", e)
            return None, None, None


def main():
    travel_mode = "WALK"
    api_key = "AIzaSyCGygp0SRJldfPq7nWt7kPNtaJ168VZH7E"  # Replace "YOUR_API_KEY" with your actual Google Maps API key
    google_maps = GoogleMaps(api_key)
    # google_maps.search_text(text_query, page_size, None)
    
    origins = PlacesDAO().read_all_locations()
    dests = PlacesDAO().read_all_locations()
    for origin in origins:
        for dest in dests:
            distance, duration, polyline = google_maps.get_distance_time(origin['latitude'], origin['longitude'],
                                                                         dest['latitude'], dest['longitude'],
                                                                         travel_mode)
            RoutesDAO().insert_route(PlacesDAO().read_id_by_location(str(origin)),
                                     PlacesDAO().read_id_by_location(str(dest)), distance, duration, polyline)


if __name__ == "__main__":
    main()
