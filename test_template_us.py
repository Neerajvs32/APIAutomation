import requests

url = "https://us1.certifyme.org/api/advanced/v2/template"

payload = {
    "template_ID": "218",  # Using existing template ID
    "name": "Sample Template Name",
    "event": "Sample Template Name"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNywiaWF0IjoxNzU4MzYyNjcwfQ.yNX03MY63wH0WYYFb4wh_4p0bMRIBUzEfktXf1QhpnU"
}

response = requests.post(url, json=payload, headers=headers)

print(f"US Server Template Creation - Status Code: {response.status_code}")
print(f"Response: {response.text}")

# If template creation works, extract the template_ID for credential creation
if response.status_code in [200, 201]:
    try:
        response_data = response.json()
        template_id = response_data.get("template_ID") or response_data.get("id")
        print(f"\n✅ Template created with ID: {template_id}")
        print("Now you can use this template ID for credential creation")
    except Exception as e:
        print(f"\n⚠️ Could not parse template ID from response: {e}")