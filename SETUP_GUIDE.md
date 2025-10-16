# Step-by-Step Setup Guide

## Part 1: Google Cloud Setup (5-10 minutes)

### Create Google Cloud Project

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "HPC Log Analyzer" and click "Create"

### Enable Google Drive API

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Google Drive API"
3. Click on it and press "Enable"

### Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in app name: "HPC Log Analyzer"
   - Add your email as developer contact
   - Click "Save and Continue" through the scopes (no scopes needed here)
   - Add your email as a test user
   - Click "Save and Continue"
4. Now create the OAuth client ID:
   - Application type: "Desktop app"
   - Name: "HPC Log MCP"
   - Click "Create"
5. Download the JSON file
6. Rename it to `credentials.json` and place it in this directory

## Part 2: Python Setup

### Install Dependencies

```bash
cd /Users/tim/interesting_projects/gdrive_hpc_mcp
pip install -r requirements.txt
```

### Test Authentication

```bash
python server.py
```

This will:
1. Open your browser for Google authentication
2. Ask you to select your Google account
3. Show a warning (click "Continue" - this is your own app)
4. Request permission to view your Google Drive files
5. Create a `token.pickle` file for future use

## Part 3: Claude Desktop Configuration

### Locate Config File

**macOS**:
```bash
open ~/Library/Application\ Support/Claude/
```

**Windows**:
```
%APPDATA%\Claude\
```

### Edit claude_desktop_config.json

Open or create `claude_desktop_config.json` and add:

```json
{
  "mcpServers": {
    "gdrive-hpc": {
      "command": "python",
      "args": ["/Users/tim/interesting_projects/gdrive_hpc_mcp/server.py"]
    }
  }
}
```

**Note**: If you already have other MCP servers configured, just add the "gdrive-hpc" entry to the existing "mcpServers" object.

### Verify Python Path

Make sure you're using the correct Python:

```bash
which python
```

Update the `command` in the config if needed (might be `python3`).

### Restart Claude Desktop

1. Completely quit Claude Desktop
2. Reopen it
3. Look for the 🔌 icon indicating MCP servers are loaded

## Part 4: Testing

In Claude Desktop, try:

```
Can you list my Google Drive files?
```

```
Search for log files in my Google Drive
```

## Troubleshooting

### "credentials.json not found"
- Make sure you downloaded the OAuth client credentials
- Verify the file is named exactly `credentials.json`
- Check it's in the same directory as `server.py`

### "Module not found" errors
- Activate your virtual environment if using one
- Run `pip install -r requirements.txt` again

### Claude Desktop doesn't show MCP tools
- Check the config file syntax (valid JSON)
- Verify the file path is absolute (not relative)
- Look at Claude Desktop logs for errors

### Authentication window doesn't open
- Check if port 0 (random port) is available
- Try running `python server.py` manually first

### "Access denied" or "Insufficient permissions"
- Re-authenticate: delete `token.pickle` and run server again
- Check that Google Drive API is enabled
- Verify you granted all requested permissions

## Security Reminders

✅ The server has read-only access
✅ Your credentials stay on your machine
✅ No data is sent to third parties
⚠️ Keep `credentials.json` and `token.pickle` private
⚠️ Don't commit them to git repositories
