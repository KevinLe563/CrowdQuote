import requests
import random
from datetime import datetime, timezone, timedelta

url = 'http://localhost:8000/api/population/'

current_pop = 0 # random.randint(0, 100)
current_time = datetime.now(timezone.utc)

# for j in range(2, 4): FOR LOCATION ID
for i in range(144):
    data = {
        "location_id": 4,
        "people_count": current_pop,
        # "timestamp": str(current_time)
    }
    x = requests.post(url, json = data)
    current_pop += random.randint(-2, 2)
    if current_pop < 0:
        current_pop = 0
    # current_time += timedelta(minutes = 10)

    print(i + 1)
    # print(x.request.body)