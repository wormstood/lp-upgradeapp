"""
Configuration management for the upgrade application.
"""

import json
import os
from typing import Any, Dict, Optional


class Config:
    """Configuration manager for the upgrade application."""

    DEFAULT_CONFIG = {
        'upgrade_type': 'app',  # app, docker, or podman
        'dry_run': False,
        'auto_confirm': False,
        'log_level': 'INFO',
        'backup_before_upgrade': True,
    }

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_file: Optional path to configuration file
        """
        self.config_file = config_file
        self.config: Dict[str, Any] = self.DEFAULT_CONFIG.copy()

        if config_file and os.path.exists(config_file):
            self.load(config_file)

    def load(self, config_file: str) -> None:
        """
        Load configuration from file.

        Args:
            config_file: Path to configuration file
        """
        try:
            with open(config_file, 'r') as f:
                loaded_config = json.load(f)
                self.config.update(loaded_config)
        except Exception as e:
            print(f"Error loading configuration: {e}")

    def save(self, config_file: Optional[str] = None) -> None:
        """
        Save configuration to file.

        Args:
            config_file: Optional path to save configuration to
        """
        target_file = config_file or self.config_file
        if not target_file:
            raise ValueError("No configuration file specified")

        try:
            with open(target_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving configuration: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key doesn't exist

        Returns:
            Configuration value
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.

        Returns:
            Configuration dictionary
        """
        return self.config.copy()
