import streamlit as st
import os
from agent import run_code_security_agent


def set_environment_variables(openai_key, portia_key):
    """Set environment variables for the current session"""
    os.environ["OPENAI_API_KEY"] = openai_key
    os.environ["PORTIA_API_KEY"] = portia_key


def run_plan(github_repo, recipient_email):
    """Run the security scan plan with the provided parameters"""
    try:
        # Call the imported function from main.py
        run_code_security_agent(github_repo, recipient_email)
        return (
            f"Security scan completed successfully! You can see the issue created in your GitHub repository. \n\n"
            f"You can also check the email sent to {recipient_email} for the issue details.",
            "",
            0,
        )
    except Exception as e:
        return f"Failed to run security scan: {e}", "", 1


def main():
    st.set_page_config(page_title="Code Security Agent", page_icon="🔒", layout="wide")

    st.title("🔒 Code Security Agent")
    st.markdown(
        "Scan GitHub repositories for security vulnerabilities and create issues automatically."
    )

    # Sidebar for API keys
    with st.sidebar:
        st.header("🔑 API Configuration")
        openai_key = st.text_input(
            "OPENAI_API_KEY", type="password", help="Enter your OpenAI API key"
        )
        portia_key = st.text_input(
            "PORTIA_API_KEY", type="password", help="Enter your Portia API key"
        )

        if st.button("Set Environment Variables"):
            if openai_key and portia_key:
                set_environment_variables(openai_key, portia_key)
                st.success("Environment variables set successfully!")
            else:
                st.error("Please provide both API keys.")

    # Main form
    with st.form("security_scan_form"):
        st.header("📋 Scan Configuration")

        recipient_email = st.text_input(
            "Recipient Email",
            placeholder="user@example.com",
            help=("Email address to receive security vulnerability notifications"),
        )

        github_repo = st.text_input(
            "GitHub Repository",
            placeholder="https://github.com/username/repository",
            help="Full URL of the GitHub repository to scan",
        )

        # Form submit button
        submit_button = st.form_submit_button("🚀 Run Plan", use_container_width=True)

        if submit_button:
            if not all([openai_key, portia_key, recipient_email, github_repo]):
                st.error("Please fill in all fields and set the API keys.")
            else:
                # Set environment variables
                set_environment_variables(openai_key, portia_key)

                # Show progress
                with st.spinner("Running security scan..."):
                    result, stderr, return_code = run_plan(github_repo, recipient_email)

                # Display results
                if return_code == 0:
                    st.success("✅ Security scan completed successfully!")

                    # Display output
                    if result:
                        st.subheader("📊 Scan Results")
                        st.code(result, language="json")

                    if stderr:
                        st.subheader("⚠️ Warnings/Info")
                        st.code(stderr)
                else:
                    st.error("❌ Security scan failed!")

                    if stderr:
                        st.subheader("🚨 Error Details")
                        st.code(stderr)

                    if result:
                        st.subheader("📋 Partial Output")
                        st.code(result)

    # Instructions
    with st.expander("📖 How to use"):
        st.markdown(
            """
        1. **Set API Keys**: Enter your OpenAI and Portia API keys in the sidebar
        2. **Configure Scan**: Provide the recipient email and GitHub repository URL
        3. **Run Scan**: Click 'Run Plan' to start the security vulnerability scan
        4. **Review Results**: The app will display scan results and create GitHub issues automatically
        
        **What happens during the scan:**
        - Fetches all files from the GitHub repository
        - Downloads and analyzes code files
        - Runs Semgrep security scan for vulnerabilities
        - Creates GitHub issues for found vulnerabilities
        - Sends email notifications to the recipient
        """
        )

    # Status indicators
    col1, col2 = st.columns(2)
    with col1:
        if openai_key:
            st.success("✅ OpenAI API Key: Set")
        else:
            st.warning("⚠️ OpenAI API Key: Not Set")

    with col2:
        if portia_key:
            st.success("✅ Portia API Key: Set")
        else:
            st.warning("⚠️ Portia API Key: Not Set")


if __name__ == "__main__":
    main()
