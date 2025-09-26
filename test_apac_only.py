import requests

# APAC server configuration - Update this token
APAC_CONFIG = {
    "url": "https://apac.platform.certifyme.dev",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2MjgzLCJpYXQiOjE3NTgzNjA2NjJ9.TJw1nZ_o6JUgmqAHWP71pD77yxRkScdf171vg5xrw-Y"
}

def test_apac_token():
    """Simple test to check if APAC token is valid"""
    print("🔍 Testing APAC Server Token Validity")
    print("=" * 40)

    headers = {
        "User-Agent": "CertifyMe-Token-Test/1.0.0",
        "Authorization": APAC_CONFIG["token"]
    }

    # Try multiple endpoints to test token validity
    test_endpoints = [
        f"{APAC_CONFIG['url']}/api/advanced/v2/folder/all/test",
        f"{APAC_CONFIG['url']}/api/advanced/v2/template/all/test"
    ]

    for url in test_endpoints:
        try:
            print(f"\nTesting endpoint: {url.split('/api/')[1]}")
            response = requests.get(url, headers=headers, timeout=10)

            print(f"Status Code: {response.status_code}")

            if response.status_code == 401:
                print("❌ TOKEN EXPIRED - Please update APAC token")
                return False
            elif response.status_code in [200, 404]:  # 404 is fine, means endpoint exists but no data
                print("✅ TOKEN VALID - Ready to use")
                return True
            else:
                print(f"⚠️ Unexpected status code: {response.status_code}")
                # Continue to next endpoint

        except requests.exceptions.RequestException as e:
            print(f"❌ Connection Error: {str(e)}")
            continue

    print("❌ All endpoints failed - check token and network")
    return False

if __name__ == "__main__":
    test_apac_token()