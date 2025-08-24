from pydantic import BaseModel, Field


class GitHubFileModel(BaseModel):
    path: str
    download_url: str


class CodeFilesModel(BaseModel):
    filename: str
    content: str


class CodeFilesListModel(BaseModel):
    files: list[CodeFilesModel]


class GitHubFileListModel(BaseModel):
    files: list[GitHubFileModel]


class GitHubIssueInput(BaseModel):
    title: str
    body: str


class GitHubIssueCreationOutput(BaseModel):
    issue_url: str


class SemgrepScanOutput(BaseModel):
    findings: str


class DownloadAndReadFilesSchema(BaseModel):
    """Schema defining the inputs for the DownloadAndReadFiles tool."""

    files: list[GitHubFileModel] = Field(
        ...,
        description="List of GitHub files with path and download_url",
    )
    download_dir: str = Field(
        "./downloaded_files",
        description="Directory where files should be downloaded",
    )
