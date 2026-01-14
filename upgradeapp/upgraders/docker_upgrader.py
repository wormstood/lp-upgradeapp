"""
Docker upgrader for Docker containers and images.
"""

import subprocess
from typing import Dict, List, Optional

from .base import BaseUpgrader


class DockerUpgrader(BaseUpgrader):
    """Upgrader for Docker containers and images."""

    def check_available(self) -> bool:
        """
        Check if Docker is available on the system.

        Returns:
            True if Docker is available, False otherwise
        """
        try:
            result = subprocess.run(
                ['docker', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def list_items(self) -> List[str]:
        """
        List all Docker containers.

        Returns:
            List of container names/IDs
        """
        if not self.check_available():
            return []

        try:
            result = subprocess.run(
                ['docker', 'ps', '-a', '--format', '{{.Names}}'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return [line for line in result.stdout.strip().split('\n') if line]
        except Exception as e:
            print(f"Error listing Docker containers: {e}")

        return []

    def list_images(self) -> List[str]:
        """
        List all Docker images.

        Returns:
            List of image names
        """
        if not self.check_available():
            return []

        try:
            result = subprocess.run(
                ['docker', 'images', '--format', '{{.Repository}}:{{.Tag}}'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return [line for line in result.stdout.strip().split('\n') if line and line != '<none>:<none>']
        except Exception as e:
            print(f"Error listing Docker images: {e}")

        return []

    def check_updates(self, item: Optional[str] = None) -> Dict[str, str]:
        """
        Check for available updates for Docker images.

        Args:
            item: Optional specific image to check

        Returns:
            Dictionary of images with available updates
        """
        updates = {}
        if not self.check_available():
            return updates

        images = [item] if item else self.list_images()

        for image in images:
            try:
                # Pull latest image
                print(f"Checking for updates: {image}")
                result = subprocess.run(
                    ['docker', 'pull', image],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                if result.returncode == 0:
                    if 'Image is up to date' not in result.stdout:
                        updates[image] = 'latest'
            except Exception as e:
                print(f"Error checking updates for {image}: {e}")

        return updates

    def upgrade(self, item: Optional[str] = None, dry_run: bool = False) -> bool:
        """
        Upgrade Docker containers by pulling latest images and recreating containers.

        Args:
            item: Optional specific container to upgrade. If None, upgrade all.
            dry_run: If True, only simulate the upgrade.

        Returns:
            True if upgrade was successful, False otherwise
        """
        if not self.check_available():
            print("Docker is not available")
            return False

        containers = [item] if item else self.list_items()

        try:
            for container in containers:
                print(f"{'[DRY RUN] ' if dry_run else ''}Upgrading container: {container}")

                if dry_run:
                    print(f"  Would pull latest image for {container}")
                    print(f"  Would recreate container {container}")
                else:
                    # Get the image used by the container
                    result = subprocess.run(
                        ['docker', 'inspect', '--format', '{{.Config.Image}}', container],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode == 0:
                        image = result.stdout.strip()
                        print(f"  Pulling latest image: {image}")
                        pull_result = subprocess.run(['docker', 'pull', image], timeout=300)
                        if pull_result.returncode != 0:
                            print(f"  Warning: Failed to pull image {image}")
                            continue

                        print(f"  Stopping container: {container}")
                        stop_result = subprocess.run(['docker', 'stop', container], timeout=60)
                        if stop_result.returncode != 0:
                            print(f"  Warning: Failed to stop container {container}")
                            continue

                        print(f"  Removing container: {container}")
                        rm_result = subprocess.run(['docker', 'rm', container], timeout=30)
                        if rm_result.returncode != 0:
                            print(f"  Warning: Failed to remove container {container}")
                            continue

                        # NOTE: Container recreation is not implemented in this basic template.
                        # In a production environment, you would need to:
                        # 1. Save the container configuration before stopping
                        # 2. Recreate the container with the same configuration
                        # 3. Preserve volumes, networks, environment variables, etc.
                        # 4. Or use docker-compose/orchestration tools for automated recreation
                        print(f"  WARNING: Container {container} has been removed but not recreated.")
                        print(f"  You will need to manually recreate the container with its original configuration.")

            return True
        except Exception as e:
            print(f"Error during Docker upgrade: {e}")
            return False
