import hashlib
import json
import os
import requests

url = "https://developer-api.nest.com/devices/thermostats/FSbxP07P7AcQcibDFZtYzrTCvDOd8X7F"

token = "c.KDMKhB3e28RftnNKrPqLSfdtsDqUq1ev0CmWz8G3548Ye0JYdK12XX6fsT4qdwawtjDqmRuFfyUcRgLqyYOqklxpMHS1TSEmNdEIUTuRo75RxuNbQk9Se5XRd9yXe6BNsPADCawX1DeyGtnI" # Update with your token

payload = "{\"target_temperature_f\": 69}"

headers = {'Authorization': 'Bearer {0}'.format(token), 'Content-Type': 'application/json'}

def goUp():
    initial_response = requests.put(url, headers=headers, data=payload, allow_redirects=False)
    if initial_response.status_code == 307:
        initial_response = requests.put(initial_response.headers['Location'], headers=headers, data=payload, allow_redirects=False)
    print(initial_response.text)

goUp();