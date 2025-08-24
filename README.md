# Code Security Agent

A powerful automated security scanning tool that analyzes GitHub repositories for vulnerabilities using Portia AI and Semgrep, automatically creating GitHub issues and sending email notifications.

## Features

- **🔍 Automated Security Scanning**: Automatically scans GitHub repositories for security vulnerabilities
- **🛡️ Semgrep Integration**: Uses industry-standard Semgrep for comprehensive security analysis
- **📝 GitHub Issue Creation**: Automatically creates detailed GitHub issues for discovered vulnerabilities
- **📧 Email Notifications**: Sends immediate email alerts to specified recipients
- **🌐 Web Interface**: User-friendly Streamlit web application for easy configuration and execution


## Architecture

The Code Security Agent follows a modular, AI-driven architecture:

```
┌────────────────-─┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI   │    │   Portia Agent  │    │  GitHub API     │
│                  │────│                 │────│                 │
│ • API Config     │    │ • Plan Builder  │    │ • File Fetching │
│ • User Input     │    │ • Tool Registry │    │ • Issue Creation│
│ • Results Display│    │ • Execution     │    │                 │
└─────────────────-┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  Custom Tools   │    │   Semgrep AI    │
                       │                 │────│                 │
                       │ • File Download │    │ • Security Scan │
                       │ • Content Read  │    │ • Vulnerability │
                       │ • Data Wrapping │    │   Detection     │
                       └─────────────────┘    └─────────────────┘
```

### Core Components

- **`agent.py`**: Main orchestration logic using Portia's PlanBuilderV2
- **`models.py`**: Pydantic data models for type safety and validation
- **`tools/`**: Custom tool implementations for file handling
- **`utils.py`**: Utility functions for GitHub URL parsing and cleanup
- **`streamlit_app.py`**: Web interface for user interaction

## QuickStart

### Prerequisites

- Python 3.12 or higher
- OpenAI API key
- Portia API key
- GitHub repository access
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd code-security-agent-using-portia
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export PORTIA_API_KEY="your-portia-api-key"
   ```

### Running the Application

#### Option 1: Web Interface (Recommended)
```bash
uv run streamlit run streamlit_app.py
```

#### Option 2: Command Line
```bash
uv run agent.py
```

## Configuration

### API Keys

The application requires two API keys:

- **OpenAI API Key**: For AI-powered analysis and issue summarization
- **Portia API Key**: For AI planning and execution orchestration

## Usage

### Web Interface Usage

1. **Launch the Streamlit app**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Configure API Keys**
   - Enter your OpenAI API key
   - Enter your Portia API key
   - Click "Set Environment Variables"

3. **Configure Scan Parameters**
   - Enter recipient email address
   - Provide GitHub repository URL
   - Click "Run Plan"

### Programmatic Usage

```python
from agent import run_code_security_agent

# Run security scan
run_code_security_agent(
    github_repo_url="https://github.com/username/repository",
    user_email="user@example.com"
)
```

### Workflow Execution

1. **Repository Analysis**: Fetches all files from the specified GitHub repository
2. **File Processing**: Downloads and processes code files for analysis
3. **Security Scanning**: Runs Semgrep scan to detect vulnerabilities
4. **Issue Creation**: Automatically creates GitHub issues for found vulnerabilities
5. **Notification**: Sends email alerts to specified recipients

### Output

- **GitHub Issues**: Detailed vulnerability reports with file locations and descriptions
- **Email Notifications**: Summary emails with issue links

## Security Features

- **Secure API Key Handling**: API keys are never stored or logged
- **Temporary File Management**: Automatic cleanup of downloaded files
- **Input Validation**: Comprehensive validation of GitHub URLs and email addresses
- **Error Handling**: Graceful error handling with user-friendly messages

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure both OpenAI and Portia API keys are valid and set
2. **GitHub Access**: Verify the repository is accessible and public
3. **File Permissions**: Ensure write permissions for temporary file creation
4. **Network Issues**: Check internet connectivity for file downloads

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
- Check the troubleshooting section
- Review the code comments
- Open a GitHub issue with detailed error information
