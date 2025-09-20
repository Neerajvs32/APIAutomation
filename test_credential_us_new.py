import requests

url = "https://us1.certifyme.org/api/v2/credential"

payload = {
    "name": "Riya Thomas",
    "template_ID": "407"  # Using the newly created template ID from US server
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNywiaWF0IjoxNzU4MzYyNjcwfQ.yNX03MY63wH0WYYFb4wh_4p0bMRIBUzEfktXf1QhpnU"
}

response = requests.post(url, json=payload, headers=headers)

print(f"US Server (New Template) - Status Code: {response.status_code}")
print(f"Response: {response.text}")