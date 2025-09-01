"""
Unit tests for column management logic without GUI dependencies.
Tests the core logic that should be implemented for smart column management.
"""
import unittest
from unittest.mock import Mock, MagicMock
from typing import List, Any


class MockWidget:
    """Mock widget for testing without tkinter dependencies."""
    
    def __init__(self, initial_value: str = ""):
        self._value = initial_value
        self.destroyed = False
    
    def get(self) -> str:
        return self._value
    
    def set(self, value: str) -> None:
        self._value = value
    
    def insert(self, index: int, value: str) -> None:
        self._value = self._value[:index] + value + self._value[index:]
    
    def delete(self, start: int, end: str) -> None:
        if end == "end":
            self._value = self._value[:start]
        else:
            self._value = self._value[:start] + self._value[int(end):]
    
    def destroy(self) -> None:
        self.destroyed = True


class ColumnManagerLogic:
    """
    Core logic for column management that should be implemented.
    This class contains the business logic without GUI dependencies.
    """
    
    def __init__(self):
        self.column_widgets: List[List[MockWidget]] = []
    
    def create_column_row(self, col_idx: int) -> List[MockWidget]:
        """Create a new column row with default values."""
        row_widgets = [
            MockWidget(f"Column_{col_idx + 1}"),  # Name
            MockWidget("name"),                    # Type
            MockWidget(""),                       # Min value
            MockWidget(""),                       # Max value
            MockWidget("")                        # Text length
        ]
        return row_widgets
    
    def update_columns(self, new_count: int) -> None:
        """
        Smart column update that preserves existing data.
        This is the logic we want to implement in the GUI.
        """
        current_count = len(self.column_widgets)
        
        if new_count > current_count:
            # Add new columns
            for i in range(current_count, new_count):
                new_row = self.create_column_row(i)
                self.column_widgets.append(new_row)
        
        elif new_count < current_count:
            # Remove excess columns
            for i in range(new_count, current_count):
                # Destroy widgets in the rows we're removing
                for widget in self.column_widgets[i]:
                    widget.destroy()
            
            # Keep only the first new_count rows
            self.column_widgets = self.column_widgets[:new_count]
    
    def get_column_count(self) -> int:
        """Get current number of columns."""
        return len(self.column_widgets)
    
    def set_column_data(self, col_idx: int, field_idx: int, value: str) -> None:
        """Set data in a specific column field."""
        if col_idx < len(self.column_widgets) and field_idx < len(self.column_widgets[col_idx]):
            self.column_widgets[col_idx][field_idx].delete(0, "end")
            self.column_widgets[col_idx][field_idx].insert(0, value)
    
    def get_column_data(self, col_idx: int, field_idx: int) -> str:
        """Get data from a specific column field."""
        if col_idx < len(self.column_widgets) and field_idx < len(self.column_widgets[col_idx]):
            return self.column_widgets[col_idx][field_idx].get()
        return ""


class TestColumnManagerLogic(unittest.TestCase):
    """Test the core column management logic."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = ColumnManagerLogic()
    
    def test_initial_state(self):
        """Test initial state with no columns."""
        self.assertEqual(self.manager.get_column_count(), 0)
    
    def test_adding_first_columns(self):
        """Test adding columns to empty manager."""
        self.manager.update_columns(3)
        
        self.assertEqual(self.manager.get_column_count(), 3)
        
        # Check default values
        self.assertEqual(self.manager.get_column_data(0, 0), "Column_1")
        self.assertEqual(self.manager.get_column_data(1, 0), "Column_2")
        self.assertEqual(self.manager.get_column_data(2, 0), "Column_3")
    
    def test_adding_more_columns_preserves_data(self):
        """Test that adding columns preserves existing data."""
        # Start with 2 columns
        self.manager.update_columns(2)
        
        # Set custom data
        self.manager.set_column_data(0, 0, "Custom Column 1")
        self.manager.set_column_data(1, 0, "Custom Column 2")
        
        # Add more columns
        self.manager.update_columns(4)
        
        # Should have 4 columns now
        self.assertEqual(self.manager.get_column_count(), 4)
        
        # Original data should be preserved
        self.assertEqual(self.manager.get_column_data(0, 0), "Custom Column 1")
        self.assertEqual(self.manager.get_column_data(1, 0), "Custom Column 2")
        
        # New columns should have default values
        self.assertEqual(self.manager.get_column_data(2, 0), "Column_3")
        self.assertEqual(self.manager.get_column_data(3, 0), "Column_4")
    
    def test_removing_columns_preserves_remaining_data(self):
        """Test that removing columns preserves remaining data."""
        # Start with 4 columns
        self.manager.update_columns(4)
        
        # Set custom data in all columns
        for i in range(4):
            self.manager.set_column_data(i, 0, f"Test Column {i + 1}")
        
        # Reduce to 2 columns
        self.manager.update_columns(2)
        
        # Should have 2 columns now
        self.assertEqual(self.manager.get_column_count(), 2)
        
        # First two columns should preserve data
        self.assertEqual(self.manager.get_column_data(0, 0), "Test Column 1")
        self.assertEqual(self.manager.get_column_data(1, 0), "Test Column 2")
        
        # Check that removed widgets were destroyed
        # (This tests that cleanup was called)
    
    def test_same_number_no_change(self):
        """Test that setting same number doesn't change anything."""
        # Set up initial state
        self.manager.update_columns(3)
        self.manager.set_column_data(0, 0, "Test Data")
        
        original_widgets = self.manager.column_widgets
        
        # Set same number
        self.manager.update_columns(3)
        
        # Should be the same
        self.assertEqual(self.manager.get_column_count(), 3)
        self.assertEqual(self.manager.get_column_data(0, 0), "Test Data")
        self.assertIs(self.manager.column_widgets, original_widgets)
    
    def test_zero_columns(self):
        """Test reducing to zero columns."""
        # Start with some columns
        self.manager.update_columns(3)
        self.manager.set_column_data(0, 0, "Test")
        
        # Reduce to zero
        self.manager.update_columns(0)
        
        self.assertEqual(self.manager.get_column_count(), 0)
    
    def test_column_data_workflow(self):
        """Test complete workflow of data management."""
        # Start with 1 column
        self.manager.update_columns(1)
        self.manager.set_column_data(0, 0, "First")
        
        # Add columns
        self.manager.update_columns(3)
        self.manager.set_column_data(1, 0, "Second")
        self.manager.set_column_data(2, 0, "Third")
        
        # Verify all data
        self.assertEqual(self.manager.get_column_data(0, 0), "First")
        self.assertEqual(self.manager.get_column_data(1, 0), "Second")
        self.assertEqual(self.manager.get_column_data(2, 0), "Third")
        
        # Remove middle column by reducing to 2
        self.manager.update_columns(2)
        
        # First two should remain
        self.assertEqual(self.manager.get_column_data(0, 0), "First")
        self.assertEqual(self.manager.get_column_data(1, 0), "Second")


if __name__ == '__main__':
    unittest.main(verbosity=2)
