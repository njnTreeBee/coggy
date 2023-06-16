import requests
import json

url = "http://localhost:8000/text_message"
payload = {
    "message": "Hello Coggy! The first AI shaman!"
}

response = requests.post(url, json=payload)

print(response.status_code)
response_data = json.loads(response.text)
print(response_data["response"])