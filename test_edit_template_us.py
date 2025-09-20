import requests

url = "https://us1.certifyme.org/api/advanced/v2/template/edit/407"  # Using the template ID we just created

payload = {
    "name": "Updated Sample Template Name",
    "description": "Updated template description"
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNywiaWF0IjoxNzU4MzYyNjcwfQ.yNX03MY63wH0WYYFb4wh_4p0bMRIBUzEfktXf1QhpnU"
}

response = requests.put(url, json=payload, headers=headers)

print(f"US Server Template Edit - Status Code: {response.status_code}")
print(f"Response: {response.text}")