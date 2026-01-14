"""
Basic tests for the upgrader base class.
"""

import unittest
from upgradeapp.upgraders.base import BaseUpgrader


class ConcreteUpgrader(BaseUpgrader):
    """Concrete implementation for testing."""

    def check_available(self) -> bool:
        return True

    def list_items(self):
        return ['item1', 'item2']

    def check_updates(self, item=None):
        return {'item1': 'v2.0'}

    def upgrade(self, item=None, dry_run=False):
        return True


class TestBaseUpgrader(unittest.TestCase):
    """Test cases for BaseUpgrader."""

    def setUp(self):
        """Set up test fixtures."""
        self.upgrader = ConcreteUpgrader()

    def test_initialization(self):
        """Test upgrader initialization."""
        self.assertIsNotNone(self.upgrader)
        self.assertEqual(self.upgrader.config, {})

    def test_initialization_with_config(self):
        """Test upgrader initialization with config."""
        config = {'key': 'value'}
        upgrader = ConcreteUpgrader(config)
        self.assertEqual(upgrader.config, config)

    def test_check_available(self):
        """Test check_available method."""
        self.assertTrue(self.upgrader.check_available())

    def test_list_items(self):
        """Test list_items method."""
        items = self.upgrader.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('item1', items)
        self.assertIn('item2', items)

    def test_check_updates(self):
        """Test check_updates method."""
        updates = self.upgrader.check_updates()
        self.assertIn('item1', updates)
        self.assertEqual(updates['item1'], 'v2.0')

    def test_upgrade(self):
        """Test upgrade method."""
        result = self.upgrader.upgrade()
        self.assertTrue(result)

    def test_validate(self):
        """Test validate method."""
        self.assertTrue(self.upgrader.validate())


if __name__ == '__main__':
    unittest.main()
