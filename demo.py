#!/usr/bin/env python3
"""
Demo script to showcase UpgradeApp functionality.
"""

import subprocess
import sys


def run_command(cmd, description):
    """Run a command and display the output."""
    print(f"\n{'=' * 70}")
    print(f"DEMO: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('=' * 70)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    print()


def main():
    """Run demo commands."""
    print("\n" + "=" * 70)
    print("UpgradeApp Demo - Basic Python Template")
    print("=" * 70)
    
    # Show help
    run_command(
        ['python3', 'main.py', '--help'],
        "Display help message"
    )
    
    # Check Docker availability
    run_command(
        ['python3', 'main.py', 'docker', 'list'],
        "List Docker containers (if Docker is available)"
    )
    
    # Check Podman availability
    run_command(
        ['python3', 'main.py', 'podman', 'list'],
        "List Podman containers (if Podman is available)"
    )
    
    # Run tests
    print("\n" + "=" * 70)
    print("DEMO: Running unit tests")
    print("=" * 70)
    subprocess.run(['python3', '-m', 'unittest', 'tests.test_base_upgrader', '-v'])
    
    print("\n" + "=" * 70)
    print("Demo completed!")
    print("=" * 70)
    print("\nThe basic Python template is ready. You can now extend it with:")
    print("  - More upgrader types")
    print("  - Additional configuration options")
    print("  - Enhanced error handling")
    print("  - More comprehensive tests")
    print("  - Web UI or interactive CLI")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()
