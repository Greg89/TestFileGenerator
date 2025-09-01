# Development Guide

## Setup for Team Members

### Initial Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd TestFileGenerator
   ```

2. **Set up virtual environment**:
   ```bash
   # Create virtual environment
   py -m venv venv
   
   # Activate virtual environment
   .\venv\Scripts\Activate.ps1
   ```

3. **Install Python dependencies**:
   ```bash
   # Install all dependencies (core + development)
   pip install -r requirements-dev.txt
   ```

3. **Verify installation**:
   ```bash
   # Test the CLI
   python cli.py --help
   
   # Test the GUI (should open window)
   python main.py
   
   # Test column management specifically (manual)
   python manual_column_test.py
   ```

### Testing

#### Run All Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test files
pytest tests/test_column_management_logic.py -v
pytest tests/test_data_generators.py -v
```

#### Test Categories

1. **Unit Tests**: Test individual components without dependencies
   - `tests/test_data_generators.py` - Data generation logic
   - `tests/test_column_management_logic.py` - Column management logic

2. **Integration Tests**: Test component interactions
   - `test_manual_column_management.py` - Manual GUI testing

3. **GUI Tests**: Currently require display/X11 
   - `tests/test_gui_main_window.py` - GUI component tests (may fail in headless environments)

### Code Quality

```bash
# Format code
black src/ tests/

# Check imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

### Architecture

- **src/models/**: Data models and configuration
- **src/generators/**: Data generation logic
- **src/gui/**: GUI components
- **src/cli/**: Command-line interface
- **src/services/**: Business logic services
- **tests/**: Test files

### Known Issues

1. **GUI Tests**: May fail in headless environments due to tkinter dependencies
2. **Column Management**: Recently fixed - preserves data when adding/removing columns
3. **Window Size**: Fixed to open with appropriate size (1000x800)

### Contributing

1. Write tests for new functionality
2. Follow TDD approach when possible
3. Update requirements files for new dependencies
4. Test both CLI and GUI interfaces
5. Ensure code passes quality checks

### Manual Testing Checklist

#### Column Management
- [ ] Start with 5 columns
- [ ] Add data to first 3 columns
- [ ] Increase to 8 columns - data preserved, new columns added
- [ ] Decrease to 3 columns - data preserved in remaining columns
- [ ] Increase to 6 columns - original data still preserved

#### Data Generation
- [ ] Generate CSV with various data types
- [ ] Generate JSON with nested structures
- [ ] Generate Excel with multiple columns
- [ ] Test large datasets (1000+ rows)

#### GUI Functionality
- [ ] Window opens at proper size
- [ ] All buttons visible and functional
- [ ] Scrolling works in column configuration
- [ ] File format selection works
- [ ] Output directory selection works
