#!/usr/bin/env python3
"""
Updated script to run the enhanced playground server.
This checks for dependencies and starts the new playground_server2.py.
"""

import sys
import subprocess
from pathlib import Path


def check_dependencies():
    """Check if required packages are installed."""
    required_packages = ["fastapi", "uvicorn", "watchdog", "jinja2"]
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\n📦 Install them with:")
        print(f"  pip install {' '.join(missing_packages)}")
        return False

    return True


def main():
    """Main entry point."""
    print("🎮 SEVDO Enhanced Playground")
    print("=" * 40)

    if not check_dependencies():
        sys.exit(1)

    # Get the directory of this script
    script_dir = Path(__file__).parent
    server_script = script_dir / "playground_server2.py"

    if not server_script.exists():
        print(f"❌ Enhanced server script not found at {server_script}")
        # Fallback to original server
        server_script = script_dir / "playground_server.py"
        if not server_script.exists():
            print(f"❌ No server script found!")
            sys.exit(1)
        else:
            print(f"⚠️  Using fallback server: {server_script}")

    print("🚀 Starting enhanced playground server...")
    print("📂 Frontend input files: playground/input_files/")
    print("📂 Backend input files: playground/backend_input_files/")
    print("🌐 Open http://localhost:8003 in your browser")
    print("📚 Backend API docs: http://localhost:8003/backend/swagger")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 40)

    try:
        # Run the server
        subprocess.run([sys.executable, str(server_script)], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server failed with exit code {e.returncode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
