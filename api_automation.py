import requests
import json
import logging
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import time

# Server configurations
SERVERS = {
    "main": "https://my.certifyme.online",
    "server2": "https://server2.certifyme.online",  # Placeholder for additional server
    "server3": "https://server3.certifyme.online"   # Placeholder for additional server
}

# JWT Token for authentication
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2MjgzLCJpYXQiOjE3NTgyNjIyNjl9.UM3Zkh3VrkJzuGB5iBI5G-RUlaNttG8IU_s-_t2SgV4"

# Expected response codes for validation
EXPECTED_SUCCESS_CODES = [200, 201, 202, 204]

class APIAutomation:
    """Comprehensive API automation for CertifyMe platform"""

    def __init__(self, server_key: str = "main"):
        self.base_url = SERVERS.get(server_key, SERVERS["main"])
        self.setup_logging()
        self.session = requests.Session()
        self.configure_headers()

    def setup_logging(self):
        log_format = '%(asctime)s | %(levelname)8s | %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'

        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            datefmt=date_format,
            handlers=[
                logging.FileHandler('api_automation.log', mode='w'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        self.logger = logging.getLogger(__name__)

    def configure_headers(self):
        self.headers_basic = {
            "Authorization": JWT_TOKEN,
            "accept": "application/json",
            "content-type": "application/json"
        }
        self.headers_operation = {
            "Authorization": JWT_TOKEN,
            "accept": "*/*"
        }

    def make_request(self, method: str, endpoint: str, headers: Dict, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Tuple[bool, int, Optional[Dict], Optional[str]]:
        """Make API request and return result"""
        url = f"{self.base_url}{endpoint}"

        try:
            self.logger.info(f"Making {method} request to {url}")

            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers, params=params, timeout=30)
            elif method.upper() == 'POST':
                response = self.session.post(url, headers=headers, json=data, timeout=30)
            elif method.upper() == 'PUT':
                response = self.session.put(url, headers=headers, json=data, timeout=30)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, headers=headers, timeout=30)
            else:
                return False, 400, None, "Unsupported HTTP method"

            success = response.status_code in EXPECTED_SUCCESS_CODES

            try:
                response_data = response.json() if response.text else {}
            except json.JSONDecodeError:
                response_data = {"raw_response": response.text}

            error_msg = None if success else response_data.get('message', 'Unknown error')

            if success:
                self.logger.info(f"Response: {response.status_code} - Success")
            else:
                self.logger.error(f"Response: {response.status_code} - Failed: {error_msg}")

            return success, response.status_code, response_data, error_msg

        except requests.exceptions.Timeout:
            self.logger.error("Request timeout")
            return False, 408, None, "Request timeout"
        except requests.exceptions.ConnectionError:
            self.logger.error("Connection error")
            return False, 503, None, "Connection error"
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return False, 500, None, f"Unexpected error: {str(e)}"

    def validate_response(self, success: bool, status_code: int, expected_code: Optional[int] = None) -> bool:
        """Validate response based on expected code"""
        if expected_code:
            return status_code == expected_code
        return success

# Basic API methods
class BasicAPIManager(APIAutomation):
    def create_credential(self, payload: Dict) -> Tuple[bool, Optional[str]]:
        endpoint = "/api/v2/credential"
        success, status, data, error = self.make_request('POST', endpoint, self.headers_basic, payload)
        if success and data:
            credential_id = data.get("credential_UID") or data.get("id") or data.get("credential_id")
            return True, credential_id
        return False, None

    def get_credential(self, credential_id: str) -> bool:
        endpoint = f"/api/v2/credential/{credential_id}"
        success, _, _, _ = self.make_request('GET', endpoint, self.headers_operation)
        return success

    def delete_credential(self, credential_id: str) -> bool:
        endpoint = f"/api/v2/credential/{credential_id}"
        success, _, _, _ = self.make_request('DELETE', endpoint, self.headers_operation)
        return success

    def edit_credential(self, credential_id: str, payload: Dict) -> bool:
        endpoint = f"/api/v2/credential/{credential_id}"
        success, _, _, _ = self.make_request('PUT', endpoint, self.headers_basic, payload)
        return success

# Template Advanced API methods
class TemplateAPIManager(APIAutomation):
    def create_template(self, payload: Dict) -> Tuple[bool, Optional[str]]:
        endpoint = "/api/advanced/v2/template"
        success, status, data, error = self.make_request('POST', endpoint, self.headers_basic, payload)
        if success and data:
            template_id = data.get("id") or data.get("template_id")
            return True, template_id
        return False, None

    def get_all_templates(self, institution_id: str) -> bool:
        endpoint = f"/api/advanced/v2/template/all/{institution_id}"
        success, _, _, _ = self.make_request('GET', endpoint, self.headers_operation)
        return success

    def copy_template(self, template_id: str, payload: Dict) -> bool:
        endpoint = f"/api/advanced/v2/template/copy/{template_id}"
        success, _, _, _ = self.make_request('POST', endpoint, self.headers_basic, payload)
        return success

    def delete_template(self, template_id: str) -> bool:
        endpoint = f"/api/advanced/v2/template/delete/{template_id}"
        success, _, _, _ = self.make_request('DELETE', endpoint, self.headers_operation)
        return success

    def edit_template(self, template_id: str, payload: Dict) -> bool:
        endpoint = f"/api/advanced/v2/template/edit/{template_id}"
        success, _, _, _ = self.make_request('PUT', endpoint, self.headers_basic, payload)
        return success

    def get_template(self, template_id: str) -> bool:
        endpoint = f"/api/advanced/v2/template/{template_id}"
        success, _, _, _ = self.make_request('GET', endpoint, self.headers_operation)
        return success

    def get_credentials_by_template(self, template_id: str) -> bool:
        endpoint = f"/api/advanced/v2/template/credentials/{template_id}"
        success, _, _, _ = self.make_request('GET', endpoint, self.headers_operation)
        return success

# Project Manager API methods
class ProjectManagerAPIManager(APIAutomation):
    def create_folder(self, payload: Dict) -> Tuple[bool, Optional[str]]:
        endpoint = "/api/advanced/v2/folder"
        success, status, data, error = self.make_request('POST', endpoint, self.headers_basic, payload)
        if success and data:
            folder_id = data.get("id") or data.get("folder_id")
            return True, folder_id
        return False, None

    def get_folder(self, folder_id: str) -> bool:
        endpoint = f"/api/advanced/v2/folder/{folder_id}"
        success, _, _, _ = self.make_request('GET', endpoint, self.headers_operation)
        return success

    def get_all_folders(self, institution_id: str) -> bool:
        endpoint = f"/api/advanced/v2/folder/all/{institution_id}"
        success, _, _, _ = self.make_request('GET', endpoint, self.headers_operation)
        return success

# Analytics API methods
class AnalyticsAPIManager(APIAutomation):
    def get_template_analytics(self, template_id: str) -> bool:
        endpoint = f"/api/advanced/v2/analytics/template/{template_id}"
        success, _, _, _ = self.make_request('GET', endpoint, self.headers_operation)
        return success

def run_api_tests():
    """Run all API tests in specified order"""
    print("=" * 60)
    print("CertifyMe API Automation Test Suite")
    print("=" * 60)

    # Test on main server
    servers_to_test = ["main"]  # Can add "server2", "server3" later

    for server in servers_to_test:
        print(f"\nTesting on server: {server.upper()}")
        print("-" * 40)

        # Initialize managers
        basic_api = BasicAPIManager(server)
        template_api = TemplateAPIManager(server)
        project_api = ProjectManagerAPIManager(server)
        analytics_api = AnalyticsAPIManager(server)

        # Test data placeholders - replace with actual data
        test_credential_payload = {"name": "Test User", "email": "test@example.com"}
        test_template_payload = {"name": "Test Template", "description": "Test description"}
        test_folder_payload = {"name": "Test Folder"}

        # Basic API Tests
        print("\n1. Basic API Tests:")

        # Create credential
        success, credential_id = basic_api.create_credential(test_credential_payload)
        print(f"   Create Credential: {'PASS' if success else 'FAIL'}")
        if not success:
            continue

        # Get credential
        success = basic_api.get_credential(credential_id)
        print(f"   Get Credential: {'PASS' if success else 'FAIL'}")

        # Edit credential
        success = basic_api.edit_credential(credential_id, {"name": "Updated Test User"})
        print(f"   Edit Credential: {'PASS' if success else 'FAIL'}")

        # Template API Tests
        print("\n2. Template Advanced API Tests:")

        # Create template
        success, template_id = template_api.create_template(test_template_payload)
        print(f"   Create Template: {'PASS' if success else 'FAIL'}")
        if not success:
            continue

        # Get all templates (need institution_id - placeholder)
        success = template_api.get_all_templates("institution_id_placeholder")
        print(f"   Get All Templates: {'PASS' if success else 'FAIL'}")

        # Get template
        success = template_api.get_template(template_id)
        print(f"   Get Template: {'PASS' if success else 'FAIL'}")

        # Get credentials by template
        success = template_api.get_credentials_by_template(template_id)
        print(f"   Get Credentials by Template: {'PASS' if success else 'FAIL'}")

        # Copy template
        success = template_api.copy_template(template_id, {"name": "Copied Template"})
        print(f"   Copy Template: {'PASS' if success else 'FAIL'}")

        # Edit template
        success = template_api.edit_template(template_id, {"name": "Updated Template"})
        print(f"   Edit Template: {'PASS' if success else 'FAIL'}")

        # Project Manager API Tests
        print("\n3. Project Manager API Tests:")

        # Create folder
        success, folder_id = project_api.create_folder(test_folder_payload)
        print(f"   Create Folder: {'PASS' if success else 'FAIL'}")
        if not success:
            continue

        # Get folder
        success = project_api.get_folder(folder_id)
        print(f"   Get Folder: {'PASS' if success else 'FAIL'}")

        # Get all folders (need institution_id - placeholder)
        success = project_api.get_all_folders("institution_id_placeholder")
        print(f"   Get All Folders: {'PASS' if success else 'FAIL'}")

        # Analytics API Tests
        print("\n4. Analytics API Tests:")

        # Get template analytics
        success = analytics_api.get_template_analytics(template_id)
        print(f"   Get Template Analytics: {'PASS' if success else 'FAIL'}")

        # Cleanup - Delete created resources
        print("\n5. Cleanup:")

        # Delete credential
        success = basic_api.delete_credential(credential_id)
        print(f"   Delete Credential: {'PASS' if success else 'FAIL'}")

        # Delete template
        success = template_api.delete_template(template_id)
        print(f"   Delete Template: {'PASS' if success else 'FAIL'}")

        # Note: Assuming folder deletion endpoint exists, but not specified
        # success = project_api.delete_folder(folder_id)
        # print(f"   Delete Folder: {'PASS' if success else 'FAIL'}")

    print("\n" + "=" * 60)
    print("API Testing Complete")
    print("Check api_automation.log for detailed logs")

if __name__ == "__main__":
    run_api_tests()