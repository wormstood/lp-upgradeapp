#!/usr/bin/env python3
"""
Main entry point for the UpgradeApp application.
"""

import argparse
import sys
from typing import Optional

from upgradeapp.upgraders import AppUpgrader, DockerUpgrader, PodmanUpgrader
from upgradeapp.utils import Config, setup_logger


def get_upgrader(upgrade_type: str, config: Optional[Config] = None):
    """
    Get the appropriate upgrader based on type.

    Args:
        upgrade_type: Type of upgrade (app, docker, podman)
        config: Optional configuration object

    Returns:
        Upgrader instance
    """
    upgraders = {
        'app': AppUpgrader,
        'docker': DockerUpgrader,
        'podman': PodmanUpgrader,
    }

    upgrader_class = upgraders.get(upgrade_type.lower())
    if not upgrader_class:
        raise ValueError(f"Unknown upgrade type: {upgrade_type}")

    return upgrader_class(config.to_dict() if config else None)


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description='UpgradeApp - Upgrade applications, Docker, and Podman containers'
    )
    parser.add_argument(
        'type',
        choices=['app', 'docker', 'podman'],
        help='Type of upgrade to perform'
    )
    parser.add_argument(
        'action',
        choices=['list', 'check', 'upgrade'],
        help='Action to perform'
    )
    parser.add_argument(
        '--item',
        help='Specific item to target (optional)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry run without making actual changes'
    )
    parser.add_argument(
        '--config',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level'
    )

    args = parser.parse_args()

    # Setup logger
    logger = setup_logger(level=args.log_level)

    # Load configuration
    config = Config(args.config) if args.config else Config()
    if args.dry_run:
        config.set('dry_run', True)

    logger.info(f"UpgradeApp - Starting {args.type} {args.action}")

    try:
        # Get the appropriate upgrader
        upgrader = get_upgrader(args.type, config)

        # Check if upgrader is available
        if not upgrader.check_available():
            logger.error(f"{args.type.capitalize()} is not available on this system")
            return 1

        # Perform the requested action
        if args.action == 'list':
            items = upgrader.list_items()
            if items:
                logger.info(f"Found {len(items)} items:")
                for item in items:
                    print(f"  - {item}")
            else:
                logger.info("No items found")

        elif args.action == 'check':
            logger.info("Checking for updates...")
            updates = upgrader.check_updates(args.item)
            if updates:
                logger.info(f"Found {len(updates)} updates available:")
                for item, version in updates.items():
                    print(f"  - {item}: {version}")
            else:
                logger.info("No updates available")

        elif args.action == 'upgrade':
            if args.dry_run:
                logger.info("Performing dry run...")
            logger.info("Starting upgrade...")
            success = upgrader.upgrade(args.item, dry_run=args.dry_run)
            if success:
                logger.info("Upgrade completed successfully")
                return 0
            else:
                logger.error("Upgrade failed")
                return 1

        return 0

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
