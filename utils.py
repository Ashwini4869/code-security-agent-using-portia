import re
import shutil
import os

from typing import Tuple


def extract_github_info(url: str) -> Tuple[str, str, str]:
    """
    Extracts the owner, repo, and path from a GitHub repository URL.
    If no path is specified, path is set to "/".
    """
    pattern = r"https?://github\.com/([^/]+)/([^/]+)(/.*)?"
    match = re.match(pattern, url)
    if not match:
        raise ValueError(f"Invalid GitHub URL: {url}")
    owner = match.group(1)
    repo = match.group(2)
    path = match.group(3) if match.group(3) else "/"
    return owner, repo, path


def cleanup_files():
    """
    Deletes the ./downloaded_files directory and all its contents if it exists.
    """

    dir_path = "./downloaded_files"
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        shutil.rmtree(dir_path)

    # Also delete all files from .portia/cache directory
    cache_dir = ".portia/cache"
    if os.path.exists(cache_dir) and os.path.isdir(cache_dir):
        shutil.rmtree(cache_dir)
