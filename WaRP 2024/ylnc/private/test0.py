URL = "http://127.0.0.1:4444/list"

import requests

response = requests.get(URL)

print(response.json())
