# lp-upgradeapp
Learn Python: Upgrade App

A Python application for upgrading system applications, Docker containers, and Podman containers based on user input.

## Features

- **Application Upgrader**: Upgrade system packages using native package managers (apt, yum, dnf, etc.)
- **Docker Upgrader**: Manage and upgrade Docker containers and images
- **Podman Upgrader**: Manage and upgrade Podman containers and images
- **Modular Architecture**: Easy to extend with new upgrader types
- **Dry Run Mode**: Test upgrades without making actual changes
- **Configurable**: JSON-based configuration support

## Project Structure

```
lp-upgradeapp/
├── upgradeapp/
│   ├── __init__.py
│   ├── upgraders/
│   │   ├── __init__.py
│   │   ├── base.py              # Base upgrader class
│   │   ├── app_upgrader.py      # Application/package upgrader
│   │   ├── docker_upgrader.py   # Docker container upgrader
│   │   └── podman_upgrader.py   # Podman container upgrader
│   └── utils/
│       ├── __init__.py
│       ├── config.py            # Configuration management
│       └── logger.py            # Logging setup
├── main.py                      # Main entry point
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
├── config.example.json          # Example configuration file
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/wormstood/lp-upgradeapp.git
cd lp-upgradeapp
```

2. Install the package (optional):
```bash
pip install -e .
```

## Usage

### Basic Commands

The application supports three main upgrade types: `app`, `docker`, and `podman`.

#### List Items

List all available items for upgrade:

```bash
# List system packages
python main.py app list

# List Docker containers
python main.py docker list

# List Podman containers
python main.py podman list
```

#### Check for Updates

Check for available updates:

```bash
# Check for package updates
python main.py app check

# Check for Docker image updates
python main.py docker check

# Check for Podman image updates
python main.py podman check
```

#### Perform Upgrades

Upgrade items:

```bash
# Upgrade all system packages
python main.py app upgrade

# Upgrade a specific package
python main.py app upgrade --item package-name

# Upgrade Docker containers (dry run)
python main.py docker upgrade --dry-run

# Upgrade a specific Podman container
python main.py podman upgrade --item container-name
```

### Command-Line Options

- `type`: Upgrade type (`app`, `docker`, `podman`)
- `action`: Action to perform (`list`, `check`, `upgrade`)
- `--item`: Specific item to target (optional)
- `--dry-run`: Perform a dry run without making actual changes
- `--config`: Path to configuration file
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

### Configuration

Create a configuration file based on `config.example.json`:

```bash
cp config.example.json config.json
```

Edit the configuration as needed and use it:

```bash
python main.py app upgrade --config config.json
```

## Examples

```bash
# List all installed packages
python main.py app list

# Check for available package updates
python main.py app check

# Perform a dry run upgrade of all packages
python main.py app upgrade --dry-run

# List all Docker containers
python main.py docker list

# Upgrade a specific Docker container
python main.py docker upgrade --item my-container

# Check Podman image updates with debug logging
python main.py podman check --log-level DEBUG
```

## Development

### Running Tests

(Tests to be implemented in future updates)

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Future Enhancements

- Add comprehensive test suite
- Implement backup functionality before upgrades
- Add support for more package managers
- Implement rollback functionality
- Add web UI for easier management
- Support for configuration via YAML
- Integration with container orchestration tools (Docker Compose, Kubernetes)
- Scheduled automatic upgrades
- Email/notification system for upgrade status

## Requirements

- Python 3.8 or higher
- Appropriate permissions for package management and container operations
- Docker (for Docker upgrader functionality)
- Podman (for Podman upgrader functionality)

## License

This project is part of a learning exercise (Learn Python: Upgrade App).

## Author

wormstood
