
import os

books_dir = "books"
file_names = []

# Walk through books directory and get all files
for _, _, files in os.walk(books_dir):
    for file in files:
        file_names.append(file)

hacked = {}

for file_name in file_names:

    URL = "http://127.0.0.1:4444/download/"
    FILE_NAME = file_name
    PASSWORD = "".join([chr(ord('a') + i % 26) for i in os.urandom(64)])

    import hashlib

    file_name_hash = hashlib.sha256(FILE_NAME.encode()).hexdigest()
    password_hash = hashlib.sha256(PASSWORD.encode()).hexdigest()
    IV = bytes.fromhex(password_hash[:32])
    url = URL + file_name_hash + "?password=" + PASSWORD

    print(url)
    import requests

    response = requests.get(url)
    response = bytes.fromhex(response.json()["message"])

    with open("ypubs/" + FILE_NAME + ".yorixpub", "wb") as f:
        f.write(response)
    
    hacked[FILE_NAME] = PASSWORD
    
with open("hacked.json", "w") as f:
    import json
    json.dump(hacked, f, indent=4)