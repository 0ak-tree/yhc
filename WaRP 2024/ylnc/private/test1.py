URL = "http://127.0.0.1:4444/download/"
FILE_NAME = "이세계로 전생했더니 순정 모험 라이프.pdf"
PASSWORD = "12345678"

import hashlib

file_hash = hashlib.sha256(FILE_NAME.encode()).hexdigest()
url = URL + file_hash + "?password=" + PASSWORD

import requests

response = requests.get(url)
print(response.json())
