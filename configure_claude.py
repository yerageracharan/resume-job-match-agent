"""Register this local MCP server in Claude Desktop on Windows/macOS/Linux."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def get_config_path() -> Path:
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise RuntimeError("APPDATA is not set. Open this script from Windows with a signed-in user profile.")
        return Path(appdata) / "Claude" / "claude_desktop_config.json"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"


def main() -> None:
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Claude config contains invalid JSON. Fix it first: {config_path}\n{exc}")
    else:
        config = {}

    servers = config.setdefault("mcpServers", {})
    if not isinstance(servers, dict):
        raise SystemExit("The mcpServers field in Claude config must be a JSON object.")
    server_path = (Path(__file__).resolve().parent / "mcp_server.py").resolve()
    python_path = Path(sys.executable).resolve()
    servers["resume-job-match"] = {
        "command": str(python_path),
        "args": [str(server_path)],
    }
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    print("Claude Desktop MCP server configured successfully.")
    print(f"Config: {config_path}")
    print(f"Python: {python_path}")
    print("Next: fully quit and restart Claude Desktop, then open Settings > Developer to check the server.")


if __name__ == "__main__":
    main()
