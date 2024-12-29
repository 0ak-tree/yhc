import requests

url = "http://127.0.0.1:4444/view"

yorixpub = open("user_dist/IMPORTANT.md.yorixpub", "rb").read()

response = requests.post(url, json={"yorixpub": yorixpub.hex(), "password": "kzeocfpbdwqpmhntahqfxdizdsfrkisrmrdfykwlwjqcolikpvdmmsivwpnmsbqv"})
try:
    response = response.json()["message"]
    print(bytes.fromhex(response))
except:
    error = response.json()["error"]
    print(error)
