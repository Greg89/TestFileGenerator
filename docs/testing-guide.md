# Testing Guide - TDD Setup

## Overview
This project uses Test-Driven Development (TDD) with pytest as the testing framework. Tests are organized to ensure robust, maintainable code with high coverage.

## Quick Start

### 1. Environment Setup
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install all dependencies including testing tools
pip install -r requirements-dev.txt
```

### 2. Running Tests
```bash
# Run all tests (excludes GUI tests by default)
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_column_management_logic.py -v

# Run with coverage report
pytest --cov=src --cov-report=html

# Include GUI tests (requires display)
pytest -k "gui" -v

# Run all tests including GUI
pytest -k "" -v
```

## Test Structure

### Test Categories

1. **Unit Tests** (`tests/test_*.py`)
   - Test individual components in isolation
   - No external dependencies (GUI, file system, network)
   - Fast execution, run frequently during development

2. **Logic Tests** (`tests/test_*_logic.py`)
   - Test business logic without GUI dependencies
   - Use mock objects to simulate UI components
   - Example: `test_column_management_logic.py`

3. **Integration Tests** (`manual_*.py` in root)
   - Test component interactions
   - May require GUI or file system
   - Example: `manual_column_test.py`

### Current Test Files

- `tests/test_data_generators.py` - Data generation logic
- `tests/test_column_management_logic.py` - Column management business logic
- `tests/test_gui_main_window.py` - GUI components (may fail in headless environments)
- `manual_column_test.py` - Manual testing script (excluded from automated tests)

## TDD Workflow

### Red-Green-Refactor Cycle

1. **Red**: Write a failing test that describes desired behavior
   ```python
   def test_adding_columns_preserves_data(self):
       # Arrange: Set up initial state
       self.manager.update_columns(2)
       self.manager.set_column_data(0, 0, "Test Data")
       
       # Act: Perform the action
       self.manager.update_columns(4)
       
       # Assert: Verify expected behavior
       assert self.manager.get_column_data(0, 0) == "Test Data"
   ```

2. **Green**: Write minimal code to make the test pass
   ```python
   def update_columns(self, new_count):
       if new_count > len(self.column_widgets):
           # Add new columns without affecting existing ones
           for i in range(len(self.column_widgets), new_count):
               self.column_widgets.append(self.create_column_row(i))
   ```

3. **Refactor**: Improve code while keeping tests green
   - Extract methods, improve naming, optimize performance
   - Run tests after each change to ensure nothing breaks

### Example TDD Session

```bash
# 1. Write failing test
pytest tests/test_new_feature.py::test_new_behavior -v
# Expected: FAILED

# 2. Implement minimal code
# Edit source files...

# 3. Run test again
pytest tests/test_new_feature.py::test_new_behavior -v
# Expected: PASSED

# 4. Refactor and verify
pytest tests/test_new_feature.py -v
# Expected: All PASSED
```

## Test Writing Guidelines

### Naming Conventions
- Test files: `test_<module_name>.py`
- Test classes: `Test<ClassName>`
- Test methods: `test_<behavior_description>`

### Test Structure (AAA Pattern)
```python
def test_feature_behavior(self):
    # Arrange: Set up test data and conditions
    manager = ColumnManager()
    manager.setup_initial_state()
    
    # Act: Execute the behavior being tested
    result = manager.perform_action()
    
    # Assert: Verify the expected outcome
    assert result == expected_value
    assert manager.state == expected_state
```

### Mocking External Dependencies
```python
from unittest.mock import Mock, patch

def test_with_mocked_service(self):
    # Mock external service
    with patch('src.gui.main_window.DataGenerationService') as mock_service:
        mock_service.return_value.get_data_types.return_value = ['name', 'email']
        
        # Test your code with the mock
        app = MainWindow()
        assert len(app.available_types) == 2
```

## Coverage and Quality

### Coverage Reports
```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# View report
# Open htmlcov/index.html in browser

# Console coverage report
pytest --cov=src --cov-report=term-missing
```

### Code Quality Checks
```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## CI/CD Integration

### Pre-commit Checks
```bash
# Run all quality checks before committing
black src/ tests/ && isort src/ tests/ && flake8 src/ tests/ && pytest
```

### GitHub Actions (example)
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    - name: Install dependencies
      run: pip install -r requirements-dev.txt
    - name: Run tests
      run: pytest --cov=src
```

## Troubleshooting

### Common Issues

1. **GUI Tests Failing in Headless Environment**
   ```bash
   # Skip GUI tests
   pytest -k "not gui"
   ```

2. **Import Errors**
   ```bash
   # Ensure you're in the project root and venv is activated
   .\venv\Scripts\Activate.ps1
   python -c "import sys; print(sys.path)"
   ```

3. **Slow Tests**
   ```bash
   # Run only fast unit tests
   pytest tests/test_*_logic.py
   
   # Profile slow tests
   pytest --durations=10
   ```

### Environment Variables
```bash
# Set test environment
$env:TESTING = "true"
pytest
```

## Best Practices

1. **Write Tests First**: Always write the test before implementing the feature
2. **One Assertion Per Test**: Each test should verify one specific behavior
3. **Descriptive Names**: Test names should clearly describe what is being tested
4. **Independent Tests**: Tests should not depend on each other
5. **Fast Feedback**: Keep unit tests fast (< 1 second each)
6. **Mock External Dependencies**: Don't test third-party libraries
7. **Test Edge Cases**: Include boundary conditions and error cases

## Examples

### Testing a New Feature
```python
# tests/test_new_export_feature.py
class TestDataExport:
    def test_export_csv_creates_file(self):
        """Test that CSV export creates a file with correct content."""
        # Arrange
        exporter = CSVExporter()
        data = [{'name': 'John', 'email': 'john@example.com'}]
        
        # Act
        result_path = exporter.export(data, 'test_output.csv')
        
        # Assert
        assert Path(result_path).exists()
        with open(result_path) as f:
            content = f.read()
            assert 'John' in content
            assert 'john@example.com' in content
```

### Manual Testing
```bash
# Run the manual test script
python manual_column_test.py

# Follow on-screen instructions to verify GUI behavior
```

This TDD setup ensures reliable, maintainable code with comprehensive test coverage.
