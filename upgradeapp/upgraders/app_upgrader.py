"""
Application upgrader for system applications and packages.
"""

import subprocess
from typing import Dict, List, Optional

from .base import BaseUpgrader


class AppUpgrader(BaseUpgrader):
    """Upgrader for system applications and packages."""

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the application upgrader.

        Args:
            config: Optional configuration dictionary
        """
        super().__init__(config)
        self.package_manager = self._detect_package_manager()

    def _detect_package_manager(self) -> Optional[str]:
        """
        Detect the system package manager.

        Returns:
            Package manager name (apt, yum, dnf, pacman, etc.) or None
        """
        managers = ['apt', 'yum', 'dnf', 'pacman', 'zypper']
        for manager in managers:
            try:
                result = subprocess.run(
                    ['which', manager],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return manager
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        return None

    def check_available(self) -> bool:
        """
        Check if package manager is available.

        Returns:
            True if package manager is available, False otherwise
        """
        return self.package_manager is not None

    def list_items(self) -> List[str]:
        """
        List all installed packages.

        Returns:
            List of installed package names
        """
        if not self.check_available():
            return []

        try:
            if self.package_manager == 'apt':
                result = subprocess.run(
                    ['dpkg', '--get-selections'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    packages = [line.split()[0] for line in result.stdout.strip().split('\n')
                               if line and 'install' in line]
                    return packages
            # Add other package managers as needed
        except Exception as e:
            print(f"Error listing packages: {e}")

        return []

    def check_updates(self, item: Optional[str] = None) -> Dict[str, str]:
        """
        Check for available updates.

        Args:
            item: Optional specific package to check

        Returns:
            Dictionary of packages with available updates
        """
        updates = {}
        if not self.check_available():
            return updates

        try:
            if self.package_manager == 'apt':
                # Update package list
                subprocess.run(
                    ['sudo', 'apt', 'update'],
                    capture_output=True,
                    timeout=60
                )
                # Check for upgradable packages
                result = subprocess.run(
                    ['apt', 'list', '--upgradable'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    for line in result.stdout.strip().split('\n')[1:]:  # Skip header
                        if line:
                            parts = line.split()
                            if len(parts) >= 2:
                                pkg_name = parts[0].split('/')[0]
                                version = parts[1]
                                if item is None or pkg_name == item:
                                    updates[pkg_name] = version
        except Exception as e:
            print(f"Error checking updates: {e}")

        return updates

    def upgrade(self, item: Optional[str] = None, dry_run: bool = False) -> bool:
        """
        Perform package upgrade.

        Args:
            item: Optional specific package to upgrade. If None, upgrade all.
            dry_run: If True, only simulate the upgrade.

        Returns:
            True if upgrade was successful, False otherwise
        """
        if not self.check_available():
            print(f"Package manager not available")
            return False

        try:
            cmd = []
            if self.package_manager == 'apt':
                cmd = ['sudo', 'apt']
                if dry_run:
                    cmd.extend(['--dry-run'])
                cmd.append('upgrade')
                if item:
                    cmd.append(item)
                else:
                    cmd.extend(['-y'])

            if cmd:
                print(f"Running: {' '.join(cmd)}")
                if not dry_run:
                    result = subprocess.run(cmd, timeout=300)
                    return result.returncode == 0
                else:
                    print("Dry run - no actual upgrade performed")
                    return True

        except Exception as e:
            print(f"Error during upgrade: {e}")
            return False

        return False
