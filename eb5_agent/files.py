# Purpose: Windows-specific file discovery in Documents\\eb5 and Dropbox\\eb5 for the given client.
import os
import glob
from typing import List, Optional

def find_client_files(client_name: str) -> List[str]:
    """
    Search all files in the client's folder across Windows Documents\\eb5 and Dropbox\\eb5.

    Example folders:
      C:\\Users\\<User>\\Documents\\eb5\\<ClientName>\\
      C:\\Users\\<User>\\Dropbox\\eb5\\<ClientName>\\
    """
    home_dir = os.path.expanduser("~")
    base_paths = [
        os.path.join(home_dir, "Documents", "eb5"),
        os.path.join(home_dir, "Dropbox", "eb5"),
    ]
    found_files = []
    for base in base_paths:
        client_folder = os.path.join(base, client_name)
        if os.path.exists(client_folder):
            files = glob.glob(os.path.join(client_folder, "**", "*.*"), recursive=True)
            found_files.extend(files)
    return found_files

def find_passport_file(files: List[str]) -> Optional[str]:
    """Return the first file that looks like a passport scan."""
    for f in files:
        fname = os.path.basename(f).lower()
        if "passport" in fname and fname.endswith((".jpg", ".jpeg", ".png", ".pdf")):
            return f
    return None