#!/bin/bash

echo "=========================================="
echo "Google Drive HPC Log Analyzer MCP Server"
echo "Installation Script"
echo "=========================================="
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Get Google Drive API credentials:"
echo "   - Go to https://console.cloud.google.com/"
echo "   - Create a project and enable Google Drive API"
echo "   - Create OAuth 2.0 credentials (Desktop app)"
echo "   - Download and save as 'credentials.json'"
echo ""
echo "2. Test the server:"
echo "   python server.py"
echo ""
echo "3. Configure Claude Desktop:"
echo "   Edit: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo ""
echo "   Add this configuration:"
echo '   {'
echo '     "mcpServers": {'
echo '       "gdrive-hpc": {'
echo '         "command": "python",'
echo "         \"args\": [\"$(pwd)/server.py\"]"
echo '       }'
echo '     }'
echo '   }'
echo ""
echo "4. Restart Claude Desktop"
echo ""
echo "See SETUP_GUIDE.md for detailed instructions"
echo "=========================================="
