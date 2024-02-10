# Functions to make requests to the django backend
# Add auth later
import requests
import json

def update_population(url, location_id, people_count, grid, img_height, img_width):
    try:
        body = {
            "location_id": location_id,
            "people_count": people_count,
            "img_height": img_height,
            "img_width": img_width,
            "grid": json.dumps(grid),
        }
        res = requests.post(url, json = body)
        print(f"POST to Server status: {res.status_code}")
        return res
    except Exception as e:
        print(f"Exception during POST: {e}")