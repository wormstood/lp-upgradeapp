# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/wormstood/lp-upgradeapp.git
cd lp-upgradeapp

# Optional: Install as a package
pip install -e .
```

## Quick Examples

### 1. List Available Items

```bash
# List system packages
python main.py app list

# List Docker containers
python main.py docker list

# List Podman containers
python main.py podman list
```

### 2. Check for Updates

```bash
# Check for package updates
python main.py app check

# Check for Docker image updates
python main.py docker check

# Check for specific item
python main.py app check --item nginx
```

### 3. Perform Upgrades

```bash
# Dry run (recommended first)
python main.py app upgrade --dry-run

# Upgrade all packages
python main.py app upgrade

# Upgrade specific item
python main.py docker upgrade --item my-container

# Use custom config
python main.py app upgrade --config config.json
```

## Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test
python -m unittest tests.test_base_upgrader -v
```

## Running Demo

```bash
python demo.py
```

## Project Structure

```
upgradeapp/
├── upgraders/          # Upgrader implementations
│   ├── base.py        # Abstract base class
│   ├── app_upgrader.py
│   ├── docker_upgrader.py
│   └── podman_upgrader.py
└── utils/             # Utility modules
    ├── config.py      # Configuration management
    └── logger.py      # Logging setup
```

## Extending the Application

### Adding a New Upgrader

1. Create a new file in `upgradeapp/upgraders/`
2. Inherit from `BaseUpgrader`
3. Implement required methods:
   - `check_available()`
   - `list_items()`
   - `check_updates()`
   - `upgrade()`
4. Add to `upgradeapp/upgraders/__init__.py`
5. Update `main.py` to include new type

Example:
```python
from upgradeapp.upgraders.base import BaseUpgrader

class MyUpgrader(BaseUpgrader):
    def check_available(self):
        # Check if tool is available
        return True
    
    def list_items(self):
        # Return list of items
        return []
    
    def check_updates(self, item=None):
        # Return dict of updates
        return {}
    
    def upgrade(self, item=None, dry_run=False):
        # Perform upgrade
        return True
```

## Configuration

Create a `config.json` file:

```json
{
  "upgrade_type": "app",
  "dry_run": false,
  "log_level": "INFO",
  "backup_before_upgrade": true
}
```

Use it:
```bash
python main.py app upgrade --config config.json
```

## Common Issues

### Permission Denied

Some operations require elevated privileges:
```bash
sudo python main.py app upgrade
```

### Docker/Podman Not Found

Ensure Docker or Podman is installed and accessible in PATH:
```bash
docker --version
podman --version
```
