# Functions to make requests to the django backend
# Add auth later
import requests

def update_population(url, location_id, people_count):
    try:
        body = {
            "location_id": location_id,
            "people_count": people_count
        }
        res = requests.post(url, json = body)
        print(f"POST to Server status: {res.status_code}")
        return res
    except Exception as e:
        print(f"Exception during POST: {e}")