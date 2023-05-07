import requests
import time

while True:
    response = requests.get('http://localhost:4000/receive')
    if response.status_code == 200:
        print(response.text)
    time.sleep(1)
