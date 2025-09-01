"""
Unit tests for the main GUI window functionality.
Tests for column management, data preservation, and user interactions.
"""
import pytest
import unittest
from unittest.mock import Mock, patch, MagicMock
import tkinter as tk
import sys
from pathlib import Path

# Mark all tests in this module as GUI tests
pytestmark = pytest.mark.gui

# Add src directory to path for imports
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from src.gui.main_window import MainWindow
from src.models.data_config import DataType, ColumnConfig


class TestMainWindowColumnManagement(unittest.TestCase):
    """Test cases for GUI column management functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock the data generation service to avoid dependencies
        with patch('src.gui.main_window.DataGenerationService') as mock_service:
            mock_service.return_value.get_available_data_types.return_value = [
                DataType.NAME, DataType.EMAIL, DataType.PHONE, DataType.INTEGER, DataType.FLOAT
            ]
            mock_service.return_value.get_available_file_formats.return_value = [
                'csv', 'json', 'xml', 'txt', 'excel'
            ]
            
            # Create a root window for testing
            self.root = tk.Tk()
            self.root.withdraw()  # Hide the window during testing
            
            # Create MainWindow instance
            self.app = MainWindow()
            self.app.root.withdraw()  # Hide the test window
            
    def tearDown(self):
        """Clean up after tests."""
        try:
            self.app.root.destroy()
            self.root.destroy()
        except:
            pass

    def test_initial_column_widgets_creation(self):
        """Test that initial column widgets are created correctly."""
        # Set initial number of columns
        self.app.columns_var.set("3")
        self.app.create_column_widgets()
        
        # Should have 3 column widget rows
        self.assertEqual(len(self.app.column_widgets), 3)
        
        # Each row should have 5 widgets (name, type, min, max, length)
        for row_widgets in self.app.column_widgets:
            self.assertEqual(len(row_widgets), 5)

    def test_adding_columns_preserves_existing_data(self):
        """Test that adding columns preserves existing configuration."""
        # Start with 2 columns
        self.app.columns_var.set("2")
        self.app.create_column_widgets()
        
        # Set some data in the first two columns
        self.app.column_widgets[0][0].insert(0, "Test Column 1")  # Name
        self.app.column_widgets[1][0].insert(0, "Test Column 2")  # Name
        
        # Store the original data
        original_name_1 = self.app.column_widgets[0][0].get()
        original_name_2 = self.app.column_widgets[1][0].get()
        
        # Increase to 4 columns
        self.app.columns_var.set("4")
        self.app.create_column_widgets()
        
        # Should now have 4 columns
        self.assertEqual(len(self.app.column_widgets), 4)
        
        # Original data should be preserved
        self.assertEqual(self.app.column_widgets[0][0].get(), original_name_1)
        self.assertEqual(self.app.column_widgets[1][0].get(), original_name_2)
        
        # New columns should have default values
        self.assertEqual(self.app.column_widgets[2][0].get(), "Column_3")
        self.assertEqual(self.app.column_widgets[3][0].get(), "Column_4")

    def test_removing_columns_preserves_remaining_data(self):
        """Test that removing columns preserves data in remaining columns."""
        # Start with 4 columns
        self.app.columns_var.set("4")
        self.app.create_column_widgets()
        
        # Set data in all columns
        test_names = ["Col1", "Col2", "Col3", "Col4"]
        for i, name in enumerate(test_names):
            self.app.column_widgets[i][0].delete(0, tk.END)
            self.app.column_widgets[i][0].insert(0, name)
        
        # Reduce to 2 columns
        self.app.columns_var.set("2")
        self.app.create_column_widgets()
        
        # Should now have 2 columns
        self.assertEqual(len(self.app.column_widgets), 2)
        
        # First two columns should preserve their data
        self.assertEqual(self.app.column_widgets[0][0].get(), "Col1")
        self.assertEqual(self.app.column_widgets[1][0].get(), "Col2")

    def test_column_widgets_same_number_no_change(self):
        """Test that setting the same number of columns doesn't recreate widgets."""
        # Start with 3 columns
        self.app.columns_var.set("3")
        self.app.create_column_widgets()
        
        # Set some test data
        self.app.column_widgets[0][0].insert(0, "Test Data")
        original_widget = self.app.column_widgets[0][0]
        
        # Set the same number of columns
        self.app.columns_var.set("3")
        self.app.create_column_widgets()
        
        # Should still have 3 columns
        self.assertEqual(len(self.app.column_widgets), 3)
        
        # Data should be preserved (widget should be the same)
        self.assertEqual(self.app.column_widgets[0][0].get(), "Test Data")

    def test_extract_column_configs(self):
        """Test extracting column configurations from GUI."""
        # Set up 2 columns with test data
        self.app.columns_var.set("2")
        self.app.create_column_widgets()
        
        # Set test data
        self.app.column_widgets[0][0].delete(0, tk.END)
        self.app.column_widgets[0][0].insert(0, "test_name")
        self.app.column_widgets[0][1].set(DataType.NAME.value)
        
        self.app.column_widgets[1][0].delete(0, tk.END)
        self.app.column_widgets[1][0].insert(0, "test_email")
        self.app.column_widgets[1][1].set(DataType.EMAIL.value)
        
        # Extract configurations
        configs = self.app.extract_column_configs()
        
        # Should have 2 configurations
        self.assertEqual(len(configs), 2)
        
        # Check first config
        self.assertEqual(configs[0].name, "test_name")
        self.assertEqual(configs[0].data_type, DataType.NAME)
        
        # Check second config
        self.assertEqual(configs[1].name, "test_email")
        self.assertEqual(configs[1].data_type, DataType.EMAIL)

    def test_on_columns_change_triggers_widget_update(self):
        """Test that changing columns variable triggers widget update."""
        # Mock the create_column_widgets method
        with patch.object(self.app, 'create_column_widgets') as mock_create:
            # Trigger the change event
            self.app.on_columns_change()
            
            # Should have called create_column_widgets
            mock_create.assert_called_once()


class TestColumnWidgetIntegration(unittest.TestCase):
    """Integration tests for column widget functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        with patch('src.gui.main_window.DataGenerationService') as mock_service:
            mock_service.return_value.get_available_data_types.return_value = [
                DataType.NAME, DataType.EMAIL, DataType.PHONE
            ]
            mock_service.return_value.get_available_file_formats.return_value = ['csv']
            
            self.root = tk.Tk()
            self.root.withdraw()
            self.app = MainWindow()
            self.app.root.withdraw()
            
    def tearDown(self):
        """Clean up after tests."""
        try:
            self.app.root.destroy()
            self.root.destroy()
        except:
            pass

    def test_complete_column_workflow(self):
        """Test complete workflow of adding, modifying, and removing columns."""
        # Start with 1 column
        self.app.columns_var.set("1")
        self.app.create_column_widgets()
        self.assertEqual(len(self.app.column_widgets), 1)
        
        # Add data to first column
        self.app.column_widgets[0][0].insert(0, "First Column")
        
        # Increase to 3 columns
        self.app.columns_var.set("3")
        self.app.create_column_widgets()
        self.assertEqual(len(self.app.column_widgets), 3)
        self.assertEqual(self.app.column_widgets[0][0].get(), "First Column")
        
        # Add data to all columns
        self.app.column_widgets[1][0].insert(0, "Second Column")
        self.app.column_widgets[2][0].insert(0, "Third Column")
        
        # Reduce to 2 columns
        self.app.columns_var.set("2")
        self.app.create_column_widgets()
        self.assertEqual(len(self.app.column_widgets), 2)
        self.assertEqual(self.app.column_widgets[0][0].get(), "First Column")
        self.assertEqual(self.app.column_widgets[1][0].get(), "Second Column")


if __name__ == '__main__':
    # Run tests with minimal output for headless environments
    unittest.main(verbosity=2, buffer=True)
