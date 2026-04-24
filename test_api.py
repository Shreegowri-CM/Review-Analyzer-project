import requests
import json

url = "http://localhost:8000/analyze"
data = {"text": "The battery is good, but the screen is bad", "rating": 4, "user_id": "123"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=data)
    print(response.json())
except Exception as e:
    print(f"Error: {e}")
