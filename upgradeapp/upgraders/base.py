"""
Base upgrader class that defines the interface for all upgraders.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class BaseUpgrader(ABC):
    """Abstract base class for all upgraders."""

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the upgrader.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}

    @abstractmethod
    def check_available(self) -> bool:
        """
        Check if the upgrade target is available on the system.

        Returns:
            True if available, False otherwise
        """
        pass

    @abstractmethod
    def list_items(self) -> List[str]:
        """
        List all items that can be upgraded.

        Returns:
            List of item names/identifiers
        """
        pass

    @abstractmethod
    def check_updates(self, item: Optional[str] = None) -> Dict[str, str]:
        """
        Check for available updates.

        Args:
            item: Optional specific item to check. If None, check all items.

        Returns:
            Dictionary mapping item names to available versions
        """
        pass

    @abstractmethod
    def upgrade(self, item: Optional[str] = None, dry_run: bool = False) -> bool:
        """
        Perform the upgrade.

        Args:
            item: Optional specific item to upgrade. If None, upgrade all items.
            dry_run: If True, only simulate the upgrade without actually performing it.

        Returns:
            True if upgrade was successful, False otherwise
        """
        pass

    def validate(self) -> bool:
        """
        Validate the upgrade configuration.

        Returns:
            True if configuration is valid, False otherwise
        """
        return True
