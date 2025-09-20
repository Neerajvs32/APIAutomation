import requests

url = "https://apac.platform.certifyme.dev/api/v2/credential"

payload = {
    "name": "Riya Thomas",
    "template_ID": "218"  # Using existing template ID as mentioned in user's code
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2MjgzLCJpYXQiOjE3NTgzNjA2NjJ9.l29MWTgCgjkyoa4a_LLxGvvpP0EyxOJcv2Vn5zvAgOo"
}

response = requests.post(url, json=payload, headers=headers)

print(f"APAC Server - Status Code: {response.status_code}")
print(f"Response: {response.text}")