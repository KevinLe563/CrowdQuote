# Functions to make requests to the django backend
# Add auth later
import requests

def update_population(url, location_id, people_count):
    body = {
        "location_id": location_id,
        "people_count": people_count
    }
    requests.post(url, json = body)