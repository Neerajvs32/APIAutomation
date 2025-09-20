import requests

# First test template creation on APAC server
url = "https://apac.platform.certifyme.dev/api/advanced/v2/template"

payload = {
    "template_ID": "218",  # Use existing template ID
    "name": "Test Template APAC",
    "event": "Test Event APAC"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2MjgzLCJpYXQiOjE3NTgzNjA2NjJ9.l29MWTgCgjkyoa4a_LLxGvvpP0EyxOJcv2Vn5zvAgOo"
}

response = requests.post(url, json=payload, headers=headers)

print(f"APAC Template Creation - Status Code: {response.status_code}")
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