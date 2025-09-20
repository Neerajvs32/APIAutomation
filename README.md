# CertifyMe API Automation System

## 🚀 Complete API Automation Solution

This system provides comprehensive API testing and automation for the CertifyMe platform, including template management, credential operations, and detailed reporting.

## 📋 Features

### ✅ **Complete API Coverage**
- **Basic APIs**: Create, Get, Edit, Delete Credentials
- **Template APIs**: Create, Get, Edit, Delete, Copy Templates
- **Credential APIs**: Link credentials to templates
- **Analytics APIs**: Template analytics and reporting
- **Folder APIs**: Project management functionality

### 🔧 **Advanced Features**
- **Stateful Automation**: Stores created IDs for reuse in subsequent operations
- **Demo Mode**: Full functionality testing without real API calls
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Email Reporting**: Automated test reports sent to stakeholders
- **Error Handling**: Robust error detection and recovery
- **Multi-Server Support**: Configurable for different environments

### 📊 **Detailed Reporting**
Automated email reports include:
- Test execution summary
- Individual test results (Pass/Fail)
- Success rates and statistics
- Execution timing and performance
- Generated IDs and test data

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7+
- `requests` library (`pip install requests`)

### Quick Start
```bash
# Clone or download the files
cd APIAutomation

# Run with demo mode (recommended for testing)
python3 cred.py

# For production use, disable demo mode in the code
# Change: manager = CredentialManager(email_manager, demo_mode=True)
# To: manager = CredentialManager(email_manager, demo_mode=False)
```

## 🔑 Configuration

### Email Settings
```python
email_config = EmailConfig(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    sender_email="your-email@gmail.com",
    sender_password="your-app-password",  # Use Gmail App Password
    recipient_email="stakeholder@example.com"
)
```

### API Configuration
```python
# Update these values in cred.py
API_TOKEN = "your-valid-jwt-token"
BASE_URL = "https://my.certifyme.online/api/v2/credential"
```

## 📁 File Structure

```
APIAutomation/
├── cred.py                 # Main automation script
├── api_automation.py       # Alternative comprehensive script
├── test_data.json         # Stores created IDs (auto-managed)
├── credential_manager.log # Detailed execution logs
├── README.md              # This documentation
└── .github/               # CI/CD workflows
```

## 🚀 Usage Modes

### 1. Demo Mode (Default)
- Uses mock API responses
- Perfect for testing the automation logic
- No real API calls or authentication needed
- Full workflow execution with realistic responses

### 2. Production Mode
- Real API calls to CertifyMe servers
- Requires valid JWT token
- Actual data creation and testing
- Comprehensive error handling

## 📊 Test Results

### Demo Mode Results
```
✅ Template created: 3e0dc1a6
✅ Get template
✅ Edit template
✅ Get credentials by template
✅ Credential created: de524b0b-106
✅ Retrieve credential
✅ Delete credential
✅ Delete template
```

### Email Report Format
```
CertifyMe API Automation Test Report
========================================

Test Summary:
• Total Tests: 8
• Passed: 8
• Failed: 0
• Success Rate: 100.0%

Test Results:
Template Operations: ✅ PASS
Credential Operations: ✅ PASS
Overall Status: ✅ ALL TESTS PASSED
```

## 🔄 Workflow Execution

The system executes tests in the following order:

1. **Template Operations**
   - Create Template
   - Get Template
   - Edit Template
   - Get Credentials by Template

2. **Credential Operations**
   - Create Credential (linked to template)
   - Retrieve Credential

3. **Cleanup Operations**
   - Delete Credential
   - Delete Template

## 🏗️ Architecture

### Core Components

#### `CredentialManager` Class
- Main automation engine
- Handles all API operations
- Manages state persistence
- Provides demo mode functionality

#### `EmailManager` Class
- SMTP email functionality
- Automated report generation
- Configurable email settings

#### `APIResponse` Dataclass
- Standardized API response handling
- Success/failure tracking
- Error message management

### State Management

The system maintains state in `test_data.json`:
```json
{
  "template_id": "abc123",
  "credential_id": "xyz456"
}
```

IDs are automatically:
- Created during successful operations
- Stored for subsequent use
- Cleared after cleanup

## 🔐 Authentication

### JWT Token Setup
1. Log into CertifyMe dashboard
2. Generate API token
3. Replace `API_TOKEN` in `cred.py`
4. Test with demo mode first

### Alternative Authentication
The system supports various auth methods:
- Bearer tokens
- API keys
- Custom headers

## 📈 Monitoring & Logging

### Log Files
- `credential_manager.log`: Detailed execution logs
- Console output: Real-time status updates
- Email reports: Stakeholder notifications

### Log Levels
- `INFO`: Successful operations
- `ERROR`: Failed operations and errors
- `WARNING`: Non-critical issues

## 🧪 Testing Strategy

### Unit Testing
- Individual API endpoint validation
- Response format verification
- Error condition handling

### Integration Testing
- End-to-end workflow execution
- State persistence validation
- Email reporting verification

### Demo Mode Testing
- Mock response validation
- Workflow logic verification
- Performance benchmarking

## 🚨 Troubleshooting

### Common Issues

#### 401 Unauthorized
```
Solution: Update JWT token in API_TOKEN variable
```

#### Email Not Sending
```
Check Gmail App Password configuration
Verify SMTP settings
```

#### Mock Mode Not Working
```
Ensure demo_mode=True in CredentialManager initialization
```

#### IDs Not Persisting
```
Check write permissions on test_data.json
Verify JSON format integrity
```

## 📈 Performance

### Demo Mode Performance
- **Execution Time**: ~0.8 seconds
- **Memory Usage**: Minimal
- **Network Calls**: None (mock responses)

### Production Mode Performance
- **Execution Time**: 2-5 seconds (depends on API response times)
- **Network Calls**: 8 API requests per run
- **State Persistence**: Automatic JSON file management

## 🔄 Continuous Integration

### GitHub Actions
- Automated testing on code changes
- Demo mode validation
- Documentation updates

### Testing Pipeline
1. Code quality checks
2. Demo mode execution
3. Mock response validation
4. Email functionality testing

## 🤝 Contributing

### Code Standards
- PEP 8 compliance
- Comprehensive docstrings
- Type hints for all functions
- Error handling best practices

### Testing Requirements
- 100% test coverage for new features
- Mock mode validation
- Real API testing (with valid credentials)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Check the troubleshooting section
- Review the logs in `credential_manager.log`
- Test with demo mode first
- Ensure valid JWT token for production use

---

**🎯 Ready to automate your CertifyMe API testing!**

Run `python3 cred.py` to start with demo mode, then configure for production use.