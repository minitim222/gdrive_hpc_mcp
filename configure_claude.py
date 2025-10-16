#!/usr/bin/env python3
"""
Helper script to configure Claude Desktop with this MCP server
"""

import json
import os
from pathlib import Path
import sys
import shutil

def get_claude_config_path():
    """Get the Claude Desktop config file path based on OS"""
    if sys.platform == "darwin":  # macOS
        return Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
    elif sys.platform == "win32":  # Windows
        return Path(os.getenv('APPDATA')) / "Claude/claude_desktop_config.json"
    else:  # Linux
        return Path.home() / ".config/Claude/claude_desktop_config.json"

def get_python_path():
    """Get the absolute path to the Python executable"""
    # Get the current Python being used
    python_path = sys.executable

    # Verify it exists
    if not Path(python_path).exists():
        # Fall back to searching PATH
        python_path = shutil.which('python3') or shutil.which('python')

    return python_path

def main():
    server_path = Path(__file__).parent / "server.py"
    config_path = get_claude_config_path()
    python_path = get_python_path()

    print("=" * 60)
    print("Claude Desktop MCP Configuration Helper")
    print("=" * 60)
    print()

    # Server config with absolute Python path
    server_config = {
        "gdrive-hpc": {
            "command": python_path,
            "args": [str(server_path.absolute())]
        }
    }

    print(f"Python path: {python_path}")
    print(f"Server location: {server_path}")
    print(f"Config location: {config_path}")
    print()

    # Check if config file exists
    if config_path.exists():
        print(f"✓ Config file exists")

        # Read existing config
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print("✗ Config file is not valid JSON")
            config = {}

        # Add or update MCP server config
        if "mcpServers" not in config:
            config["mcpServers"] = {}

        config["mcpServers"]["gdrive-hpc"] = server_config["gdrive-hpc"]

    else:
        print(f"✗ Config file doesn't exist, will create it")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config = {"mcpServers": server_config}

    # Write config
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print()
        print("✓ Configuration updated successfully!")
        print()
        print("=" * 60)
        print("Next Steps:")
        print("=" * 60)
        print("1. Restart Claude Desktop")
        print("2. Look for the 🔌 icon indicating MCP servers are loaded")
        print("3. Try asking: 'List my Google Drive files'")
        print()

    except Exception as e:
        print(f"✗ Error writing config: {e}")
        print()
        print("Manual configuration:")
        print(json.dumps(config, indent=2))

if __name__ == "__main__":
    main()
