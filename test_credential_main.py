import requests

url = "https://my.certifyme.online/api/v2/credential"

payload = {
    "name": "Riya Thomas",
    "template_ID": "27050"  # Template ID from MAIN server test
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2OTE1LCJpYXQiOjE3NTgyNzI3ODh9.ayh5q2RKoibwMjALS0nf4f0eNgjLINWmWryMpKLZOZI"
}

response = requests.post(url, json=payload, headers=headers)

print(f"MAIN Server - Status Code: {response.status_code}")
print(f"Response: {response.text}")