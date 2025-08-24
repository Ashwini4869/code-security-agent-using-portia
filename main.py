from dotenv import load_dotenv
from portia import (
    Config,
    Portia,
    DefaultToolRegistry,
    PlanBuilderV2,
    StepOutput,
    InMemoryToolRegistry,
)
from portia.cli import CLIExecutionHooks
from portia.execution_hooks import clarify_on_tool_calls

from models import (
    GitHubFileListModel,
    GitHubIssueInput,
    GitHubIssueCreationOutput,
    SemgrepScanOutput,
)
from utils import extract_github_info, cleanup_files
from tools.download_and_read_files import DownloadAndReadFiles

load_dotenv()


# TODO: Read these info from user : streamlit app
# Example usage:
github_repo_url = "https://github.com/Ashwini4869/sample-semgrep"
owner, repo, path = extract_github_info(github_repo_url)
user_email = "william21111340@gmail.com"

config = Config.from_default()
tools = DefaultToolRegistry(config=config) + InMemoryToolRegistry.from_local_tools(
    [DownloadAndReadFiles()]
)
portia = Portia(
    config=config,
    tools=tools,
    execution_hooks=CLIExecutionHooks(
        before_tool_call=clarify_on_tool_calls(
            "portia:mcp:api.githubcopilot.com:create_issue"
        )
    ),
)

plan = (
    PlanBuilderV2("Scan GitHub repo for vulnerabilities and create issues")
    # Step 1: Fetch all files from GitHub
    .invoke_tool_step(
        step_name="Fetch GitHub repo files",
        tool="portia:mcp:api.githubcopilot.com:get_file_contents",
        args={"owner": owner, "repo": repo, "path": path},
        output_schema=GitHubFileListModel,  # expect a list of files
    )
    # Step 2: For each file, fetch the raw content via download_url and wrap into
    # code_files_model
    .invoke_tool_step(
        step_name="Download and read files",
        tool="download_and_read_files",
        args={
            "files": StepOutput("Fetch GitHub repo files")
        },  # pass entire output to tool
    )
    # Step 3: Run Semgrep scan on all files
    .invoke_tool_step(
        step_name="Run Semgrep scan",
        tool="portia:mcp:mcp.semgrep.ai:semgrep_scan",
        args={
            "code_files": StepOutput("Download and read files")
        },  # extract the files list
        output_schema=SemgrepScanOutput,  # scan results
    )
    # Step 4: Summarize the findings for github issue creation
    .llm_step(
        step_name="Get GitHub issues",
        task="""Given the semgrep scan results, summarize the findings as a description
        to a github issue. The issue should be a description of the vulnerability and
        the file that it was found in. Generate a title for the issue. Return in the
        format of {'title': 'title of the issue', 'body': 'description of the
        vulnerability'}.""",
        inputs=[StepOutput("Run Semgrep scan")],
        output_schema=GitHubIssueInput,
    )
    # Step 5: Get GitHub issues title and body
    .function_step(
        step_name="Get GitHub issues title",
        function=lambda x: x.title,
        args={"x": StepOutput("Get GitHub issues")},
    )
    .function_step(
        step_name="Get GitHub issues body",
        function=lambda x: x.body,
        args={"x": StepOutput("Get GitHub issues")},
    )
    # Step 6: Create GitHub issues
    .invoke_tool_step(
        step_name="Create GitHub issues",
        tool="portia:mcp:api.githubcopilot.com:create_issue",
        args={
            "owner": owner,
            "repo": repo,
            "title": StepOutput("Get GitHub issues title"),
            "body": StepOutput("Get GitHub issues body"),
        },
        output_schema=GitHubIssueCreationOutput,  # GitHub issue creation result
    )
    # Step 7: Create email body
    .function_step(
        step_name="Create email body",
        function=lambda x: f"A security vulnerability has been detected in your repository. Please review the following issue: \n\n{x.issue_url}",
        args={
            "x": StepOutput("Create GitHub issues"),
        },
    )
    # Step 8: Send email to user
    .invoke_tool_step(
        step_name="Send email to user",
        tool="portia:google:gmail:send_email",
        args={
            "recipients": [user_email],
            "email_title": StepOutput("Get GitHub issues title"),
            "email_body": StepOutput("Create email body"),
        },
    )
    .final_output()
    .build()
)

# Run the plan
plan_run = portia.run_plan(plan)
print(f"{plan_run.model_dump_json(indent=2)}")
print("Plan Run Completed!")

# Cleanup temporary files
cleanup_files()
print("Temporary Files cleaned up!")
