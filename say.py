import requests

url = "http://0.0.0.0:8000/text_message"
data = {
  "message": "Hello MoralesCOgitoMachina, it is your creator MU! how are you?"
}

response = requests.post(url, json=data)

print(response.json())