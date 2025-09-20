#!/usr/bin/env python3
"""
Debug script to test CertifyMe API authentication
"""
import requests
import json

# Your JWT token
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2MjgzLCJpYXQiOjE3NTgyNjIyNjl9.UM3Zkh3VrkJzuGB5iBI5G-RUlaNttG8IU_s-_t2SgV4"

# Different server URLs to test
SERVERS = [
    "https://my.certifyme.online",
]

# Different auth methods to test
AUTH_METHODS = [
    {"name": "Bearer Token", "header": f"Bearer {TOKEN}"},
    {"name": "Raw Token", "header": TOKEN},
    {"name": "Token Only", "header": f"Token {TOKEN}"},
]

def test_endpoint(server, endpoint, auth_method):
    """Test a specific endpoint with specific auth"""
    url = f"{server}{endpoint}"
    headers = {
        "Authorization": auth_method["header"],
        "accept": "application/json",
        "User-Agent": "CertifyMe-Test-Script/1.0"
    }

    print(f"\n🔍 Testing: {server}{endpoint}")
    print(f"   Auth: {auth_method['name']}")

    try:
        if "template" in endpoint and endpoint.endswith("/all/test"):
            # GET request for template list
            response = requests.get(url, headers=headers, timeout=10)
        elif "template" in endpoint and not endpoint.endswith("/all/test"):
            # POST request for template creation
            data = {"name": "Test Template", "description": "Debug test template"}
            headers["content-type"] = "application/json"
            response = requests.post(url, headers=headers, json=data, timeout=10)
        else:
            # Default GET request
            response = requests.get(url, headers=headers, timeout=10)

        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")

        if response.status_code == 200:
            print("   ✅ SUCCESS!")
            return True
        elif response.status_code == 401:
            print("   ❌ 401 Unauthorized")
        elif response.status_code == 403:
            print("   ❌ 403 Forbidden")
        else:
            print(f"   ⚠️ {response.status_code}")

    except Exception as e:
        print(f"   💥 Error: {str(e)}")

    return False

def main():
    print("🔧 CertifyMe API Authentication Debug Tool")
    print("="*50)

    # Test endpoints
    endpoints = [
        "/api/advanced/v2/template/all/test",  # Simple GET test
        "/api/advanced/v2/template",           # Template creation test
    ]

    success_found = False

    for server in SERVERS:
        print(f"\n🏠 Testing Server: {server}")
        print("-" * 40)

        for auth_method in AUTH_METHODS:
            for endpoint in endpoints:
                if test_endpoint(server, endpoint, auth_method):
                    success_found = True
                    print("\n🎉 FOUND WORKING COMBINATION!")
                    print(f"   Server: {server}")
                    print(f"   Auth: {auth_method['name']}")
                    print(f"   Endpoint: {endpoint}")

    if not success_found:
        print("\n❌ No working authentication method found.")
        print("💡 Suggestions:")
        print("   1. Check if JWT token is expired")
        print("   2. Verify server URL is correct")
        print("   3. Confirm API credentials are valid")
        print("   4. Check if additional authentication is required")

if __name__ == "__main__":
    main()