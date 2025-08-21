import requests
import logging
import sys
from datetime import datetime
from typing import Dict, Optional, Tuple
import json
from dataclasses import dataclass


@dataclass
class CredentialConfig:
    """Configuration class for credential parameters."""
    template_id: str
    recipient_name: str
    recipient_email: str


@dataclass
class APIResponse:
    """Structured API response data."""
    success: bool
    status_code: int
    data: Optional[Dict] = None
    error_message: Optional[str] = None


class CredentialManager:
    """
    Professional credential management system for CertifyMe API integration.
    
    This class provides a complete workflow for credential lifecycle management
    including creation, retrieval, and deletion operations.
    """
    
    # API Configuration
    BASE_URL = "https://app.certifyme.online/api/v2/credential"
    API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1NTk5LCJpYXQiOjE3NTU3NzA0MTB9.j-E_V7atX2B0po1QU7867FRRRE6-z-F0H118PlNLuKw"
    
    # Request timeout settings
    TIMEOUT_SECONDS = 30
    
    def __init__(self):
        """Initialize the credential manager with logging configuration."""
        self._setup_logging()
        self.session = requests.Session()
        self._configure_headers()
        
    def _setup_logging(self) -> None:
        """Configure comprehensive logging for the application."""
        log_format = '%(asctime)s | %(levelname)8s | %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            datefmt=date_format,
            handlers=[
                logging.FileHandler('credential_manager.log', mode='a'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        # Suppress unnecessary requests logging
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        
        self.logger = logging.getLogger(__name__)
        
    def _configure_headers(self) -> None:
        """Configure HTTP headers for different API operations."""
        base_headers = {
            "Authorization": self.API_TOKEN,
            "User-Agent": "CertifyMe-Credential-Manager/1.0.0"
        }
        
        self.headers_create = {
            **base_headers,
            "accept": "application/json",
            "content-type": "application/json"
        }
        
        self.headers_operation = {
            **base_headers,
            "accept": "*/*"
        }
        
    def _make_request(self, method: str, url: str, headers: Dict, 
                     data: Optional[Dict] = None) -> APIResponse:
        """
        Make HTTP request with comprehensive error handling.
        
        Args:
            method: HTTP method (GET, POST, DELETE)
            url: Request URL
            headers: Request headers
            data: Request payload (for POST requests)
            
        Returns:
            APIResponse object with success status and data
        """
        try:
            if method.upper() == 'POST':
                response = self.session.post(
                    url, 
                    headers=headers, 
                    json=data, 
                    timeout=self.TIMEOUT_SECONDS
                )
            elif method.upper() == 'GET':
                response = self.session.get(
                    url, 
                    headers=headers, 
                    timeout=self.TIMEOUT_SECONDS
                )
            elif method.upper() == 'DELETE':
                response = self.session.delete(
                    url, 
                    headers=headers, 
                    timeout=self.TIMEOUT_SECONDS
                )
            else:
                return APIResponse(
                    success=False,
                    status_code=400,
                    error_message=f"Unsupported HTTP method: {method}"
                )
                
            # Parse JSON response if available
            try:
                response_data = response.json() if response.text else {}
            except json.JSONDecodeError:
                response_data = {"raw_response": response.text}
                
            return APIResponse(
                success=response.status_code in [200, 201, 204],
                status_code=response.status_code,
                data=response_data,
                error_message=None if response.status_code < 400 else response_data.get('message', 'Unknown error')
            )
            
        except requests.exceptions.Timeout:
            return APIResponse(
                success=False,
                status_code=408,
                error_message=f"Request timeout after {self.TIMEOUT_SECONDS} seconds"
            )
        except requests.exceptions.ConnectionError:
            return APIResponse(
                success=False,
                status_code=503,
                error_message="Connection error - unable to reach API server"
            )
        except Exception as e:
            return APIResponse(
                success=False,
                status_code=500,
                error_message=f"Unexpected error: {str(e)}"
            )
            
    def create_credential(self, config: CredentialConfig) -> Tuple[bool, Optional[str]]:
        """
        Create a new digital credential.
        
        Args:
            config: Credential configuration parameters
            
        Returns:
            Tuple of (success_status, credential_id)
        """
        self.logger.info("Initiating credential creation process")
        
        payload = {
            "template_ID": config.template_id,
            "name": config.recipient_name,
            "email": config.recipient_email
        }
        
        self.logger.info(f"Creating credential for: {config.recipient_name} ({config.recipient_email})")
        
        response = self._make_request('POST', self.BASE_URL, self.headers_create, payload)
        
        if not response.success:
            self.logger.error(f"Credential creation failed | Status: {response.status_code} | Error: {response.error_message}")
            return False, None
            
        # Extract credential identifier from response
        credential_id = (
            response.data.get("credential_UID") or 
            response.data.get("id") or 
            response.data.get("credential_id")
        )
        
        if not credential_id:
            self.logger.error("Credential creation failed | No credential identifier in response")
            self.logger.debug(f"Response data: {response.data}")
            return False, None
            
        self.logger.info(f"Credential created successfully | ID: {credential_id}")
        return True, credential_id
        
    def retrieve_credential(self, credential_id: str) -> bool:
        """
        Retrieve and verify credential details.
        
        Args:
            credential_id: Unique credential identifier
            
        Returns:
            Success status of the operation
        """
        self.logger.info(f"Retrieving credential | ID: {credential_id}")
        
        url = f"{self.BASE_URL}/{credential_id}"
        response = self._make_request('GET', url, self.headers_operation)
        
        if not response.success:
            self.logger.error(f"Credential retrieval failed | Status: {response.status_code} | Error: {response.error_message}")
            return False
            
        self.logger.info(f"Credential retrieved successfully | ID: {credential_id}")
        return True
        
    def delete_credential(self, credential_id: str) -> bool:
        """
        Delete a credential from the system.
        
        Args:
            credential_id: Unique credential identifier
            
        Returns:
            Success status of the operation
        """
        self.logger.info(f"Deleting credential | ID: {credential_id}")
        
        url = f"{self.BASE_URL}/{credential_id}"
        response = self._make_request('DELETE', url, self.headers_operation)
        
        if not response.success:
            self.logger.error(f"Credential deletion failed | Status: {response.status_code} | Error: {response.error_message}")
            return False
            
        self.logger.info(f"Credential deleted successfully | ID: {credential_id}")
        return True
        
    def execute_full_workflow(self, config: CredentialConfig) -> bool:
        """
        Execute the complete credential lifecycle workflow.
        
        This method performs the full workflow:
        1. Create credential
        2. Retrieve credential (verification)
        3. Delete credential (cleanup)
        
        Args:
            config: Credential configuration parameters
            
        Returns:
            Success status of the complete workflow
        """
        workflow_start = datetime.now()
        self.logger.info("=" * 80)
        self.logger.info("WORKFLOW EXECUTION INITIATED")
        self.logger.info(f"Template ID: {config.template_id} | Recipient: {config.recipient_name}")
        self.logger.info("=" * 80)
        
        try:
            # Phase 1: Create Credential
            self.logger.info("PHASE 1: Credential Creation")
            success, credential_id = self.create_credential(config)
            
            if not success:
                self.logger.error("WORKFLOW FAILED | Credential creation unsuccessful")
                return False
                
            # Phase 2: Retrieve Credential
            self.logger.info("PHASE 2: Credential Verification")
            if not self.retrieve_credential(credential_id):
                self.logger.error("WORKFLOW FAILED | Credential verification unsuccessful")
                return False
                
            # Phase 3: Delete Credential
            self.logger.info("PHASE 3: Credential Cleanup")
            if not self.delete_credential(credential_id):
                self.logger.error("WORKFLOW FAILED | Credential cleanup unsuccessful")
                return False
                
            workflow_duration = (datetime.now() - workflow_start).total_seconds()
            self.logger.info("=" * 80)
            self.logger.info(f"WORKFLOW COMPLETED SUCCESSFULLY | Duration: {workflow_duration:.2f}s")
            self.logger.info("=" * 80)
            
            return True
            
        except Exception as e:
            self.logger.error(f"WORKFLOW FAILED | Unexpected error: {str(e)}")
            return False


def main():
    """
    Main application entry point.
    
    Configures and executes the credential management workflow.
    """
    print("CertifyMe Credential Management System")
    print("=" * 50)
    
    # Initialize credential manager
    manager = CredentialManager()
    
    # Configure credential parameters
    config = CredentialConfig(
        template_id="26613",
        recipient_name="karan",
        recipient_email="neerajsalehittal3235@gmail.com"
    )
    
    # Execute workflow
    try:
        success = manager.execute_full_workflow(config)
        
        if success:
            print("\n✅ Credential workflow completed successfully")
            sys.exit(0)
        else:
            print("\n❌ Credential workflow failed - check logs for details")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Workflow interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Critical error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()