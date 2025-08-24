from pathlib import Path
import requests
import pandas as pd
import json
from pydantic import BaseModel

from models import DownloadAndReadFilesSchema, GitHubFileModel
from portia.tool import Tool, ToolRunContext


class DownloadAndReadFiles(Tool):
    """Downloads GitHub files, reads content, and wraps as CodeFilesModel."""

    id: str = "download_and_read_files"
    name: str = "Download and Read Files"
    description: str = (
        "Downloads files from GitHub and reads them into code files model"
    )
    args_schema: type[BaseModel] = DownloadAndReadFilesSchema
    output_schema: tuple[str, str] = (
        "SemgrepCodeFilesModel",
        "A list of dictionaries with filename and content for semgrep",
    )

    def run(
        self,
        _: ToolRunContext,
        files,  # Accept any type to debug what we're actually getting
        download_dir: str = "./downloaded_files",
    ) -> list[dict]:
        Path(download_dir).mkdir(exist_ok=True, parents=True)

        # Debug: print what we received
        print(f"DEBUG: Received files input of type {type(files)}: {files}")

        code_files = []

        # Handle different input formats - GitHub tool might return different structures
        if isinstance(files, dict):
            if "files" in files:
                # GitHub tool returned {files: [...]}
                files_list = [
                    GitHubFileModel(**f) if isinstance(f, dict) else f
                    for f in files["files"]
                ]
            elif "path" in files and "download_url" in files:
                # Single file as dict
                files_list = [GitHubFileModel(**files)]
            else:
                # Unknown dict structure, try to extract files
                files_list = []
                for key, value in files.items():
                    if isinstance(value, list):
                        files_list.extend(
                            [
                                GitHubFileModel(**f) if isinstance(f, dict) else f
                                for f in value
                            ]
                        )
                    elif (
                        isinstance(value, dict)
                        and "path" in value
                        and "download_url" in value
                    ):
                        files_list.append(GitHubFileModel(**value))
        elif isinstance(files, GitHubFileModel):
            # Single file as model
            files_list = [files]
        elif isinstance(files, list):
            # List of files
            files_list = [
                GitHubFileModel(**f) if isinstance(f, dict) else f for f in files
            ]
        elif hasattr(files, "files") and isinstance(files.files, list):
            # GitHubFileListModel or similar object with a 'files' attribute
            files_list = [
                GitHubFileModel(**f) if isinstance(f, dict) else f for f in files.files
            ]
        else:
            raise ValueError(f"Unexpected files type: {type(files)}, value: {files}")

        if not files_list:
            raise ValueError("No valid files found in input")

        for file in files_list:
            file_path = Path(download_dir) / Path(file.path).name

            # Download the file
            response = requests.get(file.download_url)
            if response.status_code != 200:
                raise Exception(f"Failed to download {file.download_url}")
            file_path.write_bytes(response.content)

            # Read the file content
            suffix = file_path.suffix.lower()
            if suffix in [".txt", ".log"]:
                content = file_path.read_text(encoding="utf-8")
            elif suffix == ".csv":
                content = pd.read_csv(file_path).to_string()
            elif suffix in [".xls", ".xlsx"]:
                content = pd.read_excel(file_path).to_string()
            elif suffix == ".json":
                with file_path.open("r", encoding="utf-8") as f:
                    content = json.load(f)
            else:
                content = file_path.read_text(encoding="utf-8")

            # Return in format semgrep expects: list of dicts
            code_files.append({"filename": file.path, "content": content})

        return code_files
