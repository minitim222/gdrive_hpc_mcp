# Google Drive HPC Log Analyzer

A Model Context Protocol (MCP) server that brings Google Drive integration to Claude Desktop, with specialized tools for analyzing High Performance Computing (HPC) log files.

## Overview

This MCP server enables Claude to directly access your Google Drive files and intelligently analyze HPC job logs, helping you quickly identify errors, warnings, and resource issues without leaving the Claude Desktop interface.

## Features

- **Google Drive Integration**: Search, list, and read files directly from Google Drive
- **HPC Log Analysis**: Automatic detection of common HPC issues:
  - Out of memory (OOM) errors
  - Job timeouts and time limit issues
  - Failed jobs and fatal errors
  - Resource allocation problems
- **Smart Search**: Quickly find log files (.log, .out, .err) across your Drive
- **Read-Only Access**: Secure, read-only access to your Google Drive
- **Persistent Authentication**: One-time OAuth setup with automatic token refresh

## Prerequisites

- Python 3.7+
- Claude Desktop installed
- Google Cloud account (free tier works fine)
- pip for package management

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/minitim222/gdrive_hpc_mcp.git
cd gdrive_hpc_mcp
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Google Cloud Credentials

Follow the detailed [SETUP_GUIDE.md](SETUP_GUIDE.md) to:
1. Create a Google Cloud project
2. Enable the Google Drive API
3. Download OAuth credentials as `credentials.json`

### 4. Configure Claude Desktop

Run the automatic configuration script:

```bash
python configure_claude.py
```

Or manually edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gdrive-hpc": {
      "command": "python",
      "args": ["/absolute/path/to/gdrive_hpc_mcp/server.py"]
    }
  }
}
```

### 5. Authenticate

Run the server once to authenticate:

```bash
python server.py
```

This will open your browser for Google OAuth authentication.

### 6. Restart Claude Desktop

Quit and restart Claude Desktop. Look for the 🔌 icon to confirm the MCP server is loaded.

## Usage Examples

Once set up, you can ask Claude things like:

```
"Search for log files in my Google Drive"
```

```
"Analyze the latest job.log file and tell me why it failed"
```

```
"Find all HPC logs from last week"
```

```
"Read the error log from my simulations folder"
```

## Available Tools

The MCP server provides these tools to Claude:

### `list_drive_files`
Search and list files in Google Drive with optional queries and folder filtering.

**Parameters:**
- `query` (str): Search query (e.g., "name contains 'log'")
- `max_results` (int): Maximum number of results (default: 10)
- `folder_id` (str, optional): Specific folder ID to search within

### `read_drive_file`
Read the contents of a file from Google Drive.

**Parameters:**
- `file_id` (str): Google Drive file ID

### `analyze_hpc_log`
Analyze an HPC log file and provide insights.

**Parameters:**
- `file_id` (str): Google Drive file ID of the log file

**Returns:**
- File metadata (name, size, line count)
- List of errors found
- List of warnings found
- Actionable suggestions for fixing issues

### `search_hpc_logs`
Search specifically for HPC log files (.log, .out, .err extensions).

**Parameters:**
- `search_term` (str): Search term (default: "*.log")
- `folder_id` (str, optional): Folder to search within
- `max_results` (int): Maximum results (default: 20)

## Security

- **Read-Only Access**: The server only requests read permissions to Google Drive
- **Local Credentials**: All authentication tokens are stored locally on your machine
- **No Third-Party Access**: Your Google Drive data is accessed directly by Claude running locally
- **Gitignored Secrets**: `credentials.json` and `token.pickle` are excluded from version control

**Important**: Never commit `credentials.json` or `token.pickle` to public repositories.

## File Structure

```
gdrive_hpc_mcp/
├── server.py              # Main MCP server
├── configure_claude.py    # Claude Desktop config helper
├── test_auth.py          # Authentication test script
├── install.sh            # Installation script
├── requirements.txt      # Python dependencies
├── SETUP_GUIDE.md       # Detailed setup instructions
├── README.md            # This file
├── .gitignore           # Excludes credentials
└── credentials.json     # Your OAuth credentials (not in repo)
```

## Troubleshooting

### "credentials.json not found"
Make sure you've downloaded the OAuth client credentials from Google Cloud Console and placed them in the project directory.

### "Module not found" errors
Install dependencies: `pip install -r requirements.txt`

### MCP tools don't appear in Claude
- Verify `claude_desktop_config.json` syntax is valid JSON
- Check that the file path is absolute, not relative
- Restart Claude Desktop completely

### Authentication issues
Delete `token.pickle` and run `python server.py` to re-authenticate.

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for more detailed troubleshooting.

## Development

### Testing Authentication

```bash
python test_auth.py
```

### Running the Server Directly

```bash
python server.py
```

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

MIT License - feel free to use and modify as needed.

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Claude Desktop](https://claude.ai/desktop)
- [Google Drive API Documentation](https://developers.google.com/drive/api)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)

## Acknowledgments

Built with [FastMCP](https://github.com/jlowin/fastmcp) - a Python framework for creating MCP servers.
