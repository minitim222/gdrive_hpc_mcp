#!/usr/bin/env python3
"""
Test script to trigger Google Drive authentication
This will open your browser for the OAuth flow
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the get_drive_service function from server
from server import get_drive_service

def main():
    print("=" * 60)
    print("Google Drive Authentication Test")
    print("=" * 60)
    print()
    print("This will authenticate you with Google Drive.")
    print("Your browser will open for the OAuth flow.")
    print()

    try:
        print("Attempting to connect to Google Drive...")
        service = get_drive_service()
        print("✓ Authentication successful!")
        print()

        # Test by listing a few files
        print("Testing API access by listing files...")
        results = service.files().list(
            pageSize=5,
            fields="files(id, name)"
        ).execute()

        files = results.get('files', [])

        if not files:
            print("No files found in your Google Drive.")
        else:
            print(f"Found {len(files)} files:")
            for file in files:
                print(f"  - {file['name']} (ID: {file['id']})")

        print()
        print("=" * 60)
        print("✓ Setup Complete!")
        print("=" * 60)
        print()
        print("You can now configure Claude Desktop:")
        print("  python configure_claude.py")
        print()

    except FileNotFoundError as e:
        print("✗ Error:", str(e))
        print()
        print("Please download credentials.json from Google Cloud Console:")
        print("  1. Go to https://console.cloud.google.com/")
        print("  2. Enable Google Drive API")
        print("  3. Create OAuth 2.0 credentials (Desktop app)")
        print("  4. Download and save as 'credentials.json'")
        print()

    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
