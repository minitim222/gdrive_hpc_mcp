#!/usr/bin/env python3
"""
Google Drive HPC Logs MCP Server
Provides tools to access Google Drive and analyze HPC log files
"""

import os
import io
from pathlib import Path
from typing import Optional
import json

from fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Initialize FastMCP server
mcp = FastMCP("gdrive-hpc-analyzer")

def get_drive_service():
    """Authenticate and return Google Drive service"""
    creds = None
    token_path = Path(__file__).parent / 'token.pickle'
    credentials_path = Path(__file__).parent / 'credentials.json'

    # The file token.pickle stores the user's access and refresh tokens
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                raise FileNotFoundError(
                    f"credentials.json not found at {credentials_path}. "
                    "Please download it from Google Cloud Console."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)


@mcp.tool()
def list_drive_files(
    query: str = "",
    max_results: int = 10,
    folder_id: Optional[str] = None
) -> str:
    """
    List files in Google Drive

    Args:
        query: Search query (e.g., "name contains 'log'")
        max_results: Maximum number of results to return
        folder_id: Optional folder ID to search within

    Returns:
        JSON string with list of files
    """
    try:
        service = get_drive_service()

        # Build query
        search_query = query
        if folder_id:
            folder_query = f"'{folder_id}' in parents"
            search_query = f"{folder_query} and {query}" if query else folder_query

        # Execute search
        results = service.files().list(
            q=search_query,
            pageSize=max_results,
            fields="files(id, name, mimeType, modifiedTime, size, parents)"
        ).execute()

        files = results.get('files', [])

        if not files:
            return json.dumps({"message": "No files found", "files": []})

        return json.dumps({
            "message": f"Found {len(files)} file(s)",
            "files": files
        }, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def read_drive_file(file_id: str) -> str:
    """
    Read content from a Google Drive file

    Args:
        file_id: Google Drive file ID

    Returns:
        File content as string
    """
    try:
        service = get_drive_service()

        # Get file metadata
        file_metadata = service.files().get(fileId=file_id, fields='name,mimeType').execute()

        # Download file content
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        # Get content as string
        content = fh.getvalue().decode('utf-8', errors='ignore')

        return f"File: {file_metadata['name']}\n{'='*60}\n{content}"

    except Exception as e:
        return f"Error reading file: {str(e)}"


@mcp.tool()
def analyze_hpc_log(file_id: str) -> str:
    """
    Read and analyze an HPC log file from Google Drive

    Args:
        file_id: Google Drive file ID of the HPC log

    Returns:
        Analysis and suggestions for the HPC log
    """
    try:
        service = get_drive_service()

        # Get file metadata
        file_metadata = service.files().get(fileId=file_id, fields='name,mimeType').execute()

        # Download file content
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        # Get content as string
        content = fh.getvalue().decode('utf-8', errors='ignore')

        # Perform analysis
        analysis = {
            "file_name": file_metadata['name'],
            "file_size": len(content),
            "line_count": len(content.split('\n')),
            "content": content[:5000],  # First 5000 chars
            "truncated": len(content) > 5000
        }

        # Look for common HPC log patterns
        errors = []
        warnings = []
        suggestions = []

        for i, line in enumerate(content.split('\n'), 1):
            line_lower = line.lower()

            # Check for errors
            if any(term in line_lower for term in ['error', 'failed', 'fatal', 'exception']):
                errors.append(f"Line {i}: {line.strip()}")

            # Check for warnings
            if 'warning' in line_lower or 'warn' in line_lower:
                warnings.append(f"Line {i}: {line.strip()}")

            # Job-specific patterns
            if 'out of memory' in line_lower or 'oom' in line_lower:
                suggestions.append("Consider increasing memory allocation")
            if 'timeout' in line_lower or 'time limit' in line_lower:
                suggestions.append("Consider increasing time limit for the job")
            if 'killed' in line_lower:
                suggestions.append("Job was killed - check resource limits and usage")

        analysis['errors'] = errors[:10]  # Limit to first 10
        analysis['warnings'] = warnings[:10]
        analysis['suggestions'] = list(set(suggestions))

        return json.dumps(analysis, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def search_hpc_logs(
    search_term: str = "*.log",
    folder_id: Optional[str] = None,
    max_results: int = 20
) -> str:
    """
    Search for HPC log files in Google Drive

    Args:
        search_term: Term to search for (default: "*.log")
        folder_id: Optional folder ID to search within
        max_results: Maximum number of results

    Returns:
        JSON string with matching log files
    """
    # Build query for log files
    if search_term == "*.log":
        query = "name contains '.log' or name contains '.out' or name contains '.err'"
    else:
        query = f"name contains '{search_term}'"

    return list_drive_files(query=query, max_results=max_results, folder_id=folder_id)


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
