import requests
import logging
import sys
from datetime import datetime
from typing import Dict, Optional, Tuple
import json
from dataclasses import dataclass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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


@dataclass
class EmailConfig:
    """Configuration for SMTP email sending."""
    smtp_server: str
    smtp_port: int
    sender_email: str
    sender_password: str
    recipient_email: str


class EmailManager:
    """Handles email sending for workflow status notifications."""
    
    def __init__(self, config: EmailConfig):
        self.config = config

    def send_email(self, subject: str, body: str) -> None:
        """Send an email with given subject and body."""
        msg = MIMEMultipart()
        msg["From"] = self.config.sender_email
        msg["To"] = self.config.recipient_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                server.starttls()
                server.login(self.config.sender_email, self.config.sender_password)
                server.send_message(msg)
        except Exception as e:
            print(f"⚠️ Email sending failed: {str(e)}")


class CredentialManager:
    """
    Credential management system for CertifyMe API integration.
    """

    BASE_URL = "https://app.certifyme.online/api/v2/credential"
    API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1NTk5LCJpYXQiOjE3NTU3NzA0MTB9.j-E_V7atX2B0po1QU7867FRRRE6-z-F0H118PlNLuKw"
    TIMEOUT_SECONDS = 30

    def __init__(self, email_manager: EmailManager):
        self._setup_logging()
        self.session = requests.Session()
        self._configure_headers()
        self.email_manager = email_manager

    def _setup_logging(self) -> None:
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
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        self.logger = logging.getLogger(__name__)

    def _configure_headers(self) -> None:
        base_headers = {
            "Authorization": self.API_TOKEN,
            "User-Agent": "CertifyMe-Credential-Manager/1.0.0"
        }
        self.headers_create = {**base_headers, "accept": "application/json", "content-type": "application/json"}
        self.headers_operation = {**base_headers, "accept": "*/*"}

    def _make_request(self, method: str, url: str, headers: Dict, data: Optional[Dict] = None) -> APIResponse:
        try:
            if method.upper() == 'POST':
                response = self.session.post(url, headers=headers, json=data, timeout=self.TIMEOUT_SECONDS)
            elif method.upper() == 'GET':
                response = self.session.get(url, headers=headers, timeout=self.TIMEOUT_SECONDS)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, headers=headers, timeout=self.TIMEOUT_SECONDS)
            else:
                return APIResponse(False, 400, error_message=f"Unsupported method: {method}")

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
            return APIResponse(False, 408, error_message="Request Timeout")
        except requests.exceptions.ConnectionError:
            return APIResponse(False, 503, error_message="Connection Error")
        except Exception as e:
            return APIResponse(False, 500, error_message=f"Unexpected error: {str(e)}")

    def create_credential(self, config: CredentialConfig) -> Tuple[bool, Optional[str]]:
        payload = {"template_ID": config.template_id, "name": config.recipient_name, "email": config.recipient_email}
        response = self._make_request('POST', self.BASE_URL, self.headers_create, payload)
        if not response.success:
            return False, None
        credential_id = response.data.get("credential_UID") or response.data.get("id") or response.data.get("credential_id")
        return (True, credential_id) if credential_id else (False, None)

    def retrieve_credential(self, credential_id: str) -> bool:
        url = f"{self.BASE_URL}/{credential_id}"
        response = self._make_request('GET', url, self.headers_operation)
        return response.success

    def delete_credential(self, credential_id: str) -> bool:
        url = f"{self.BASE_URL}/{credential_id}"
        response = self._make_request('DELETE', url, self.headers_operation)
        return response.success

    def execute_full_workflow(self, config: CredentialConfig) -> bool:
        workflow_start = datetime.now()
        credential_id = None

        try:
            # Phase 1: Create
            success, credential_id = self.create_credential(config)
            if not success:
                self._send_failure_email("Credential creation failed")
                return False

            # Phase 2: Retrieve
            if not self.retrieve_credential(credential_id):
                self._send_failure_email("Credential retrieval failed", credential_id)
                return False

            # Phase 3: Delete
            if not self.delete_credential(credential_id):
                self._send_failure_email("Credential deletion failed", credential_id)
                return False

            duration = (datetime.now() - workflow_start).total_seconds()
            self._send_success_email(credential_id, duration)
            return True

        except Exception as e:
            self._send_failure_email(f"Unexpected error: {str(e)}", credential_id)
            return False

    def _send_success_email(self, credential_id: str, duration: float):
        subject = "✅ Credential Workflow Completed Successfully"
        body = (
            f"The credential workflow executed successfully.\n\n"
            f"Credential ID: {credential_id}\n"
            f"Status: Created, Retrieved, and Deleted successfully.\n"
            f"Total Duration: {duration:.2f}s\n"
        )
        self.email_manager.send_email(subject, body)

    def _send_failure_email(self, error_message: str, credential_id: Optional[str] = None):
        subject = "❌ Credential Workflow Failed"
        body = (
            f"The credential workflow encountered a failure.\n\n"
            f"Error: {error_message}\n"
            f"Credential ID: {credential_id if credential_id else 'N/A'}\n"
        )
        self.email_manager.send_email(subject, body)


def main():
    print("CertifyMe Credential Management System")
    print("=" * 50)

    # Email configuration (replace with real values)
    email_config = EmailConfig(
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        sender_email="neerajsalehittal3235@gmail.com",
        sender_password="qvkm odse mvjt rlei",  # Use App Password if Gmail
        recipient_email="neeraj@certifyme.cc"
    )
    email_manager = EmailManager(email_config)

    manager = CredentialManager(email_manager)

    config = CredentialConfig(
        template_id="26613",
        recipient_name="karan",
        recipient_email="neerajsalehittal3235@gmail.com"
    )

    success = manager.execute_full_workflow(config)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
