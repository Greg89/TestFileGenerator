# Project Structure

This document describes the organization of the Test Data Generator application.

## Directory Structure

```
TestFileGenerator/
├── src/                           # Source code package
│   ├── __init__.py               # Package initialization
│   ├── models/                   # Data models and configuration
│   │   ├── __init__.py
│   │   └── data_config.py        # Pydantic models for configuration
│   ├── generators/               # Data and file generation strategies
│   │   ├── __init__.py
│   │   ├── data_generator.py     # Data type generators (Strategy Pattern)
│   │   └── file_generators.py    # File format generators (Strategy Pattern)
│   ├── services/                 # Business logic services
│   │   ├── __init__.py
│   │   └── data_generation_service.py  # Main orchestration service
│   ├── gui/                      # Graphical user interface
│   │   ├── __init__.py
│   │   └── main_window.py        # Main GUI window
│   └── cli/                      # Command-line interface
│       ├── __init__.py
│       └── cli_generator.py      # CLI implementation
├── tests/                        # Unit tests
│   ├── __init__.py
│   └── test_data_generators.py   # Tests for data generators
├── examples/                     # Example scripts and usage
│   └── generate_sample_data.py   # Programmatic usage examples
├── main.py                       # GUI application entry point
├── cli.py                        # CLI application entry point
├── requirements.txt               # Python dependencies
├── README.md                     # Project documentation
└── PROJECT_STRUCTURE.md          # This file
```

## Architecture Overview

### Design Patterns Used

1. **Strategy Pattern**: Used for both data generation and file format generation
   - `DataGeneratorStrategy`: Abstract base for different data types
   - `FileGeneratorStrategy`: Abstract base for different file formats

2. **Factory Pattern**: Used to create appropriate generators
   - `DataGeneratorFactory`: Creates data type generators
   - `FileGeneratorFactory`: Creates file format generators

3. **Command Pattern**: Used for file generation operations

### SOLID Principles Implementation

1. **Single Responsibility Principle (SRP)**:
   - Each class has one reason to change
   - `DataGenerationService` orchestrates, `DataGeneratorStrategy` generates data, etc.

2. **Open/Closed Principle (OCP)**:
   - New data types can be added without modifying existing code
   - New file formats can be added by implementing `FileGeneratorStrategy`

3. **Liskov Substitution Principle (LSP)**:
   - All generators can be used interchangeably through their base classes

4. **Interface Segregation Principle (ISP)**:
   - Clean, focused interfaces for each responsibility

5. **Dependency Inversion Principle (DIP)**:
   - High-level modules depend on abstractions, not concrete implementations

### Key Components

#### Models (`src/models/`)
- **`DataType`**: Enum of available data types (name, email, phone, etc.)
- **`ColumnConfig`**: Configuration for individual columns
- **`FileConfig`**: Configuration for file generation
- **`GenerationRequest`**: Complete generation request

#### Data Generators (`src/generators/data_generator.py`)
- **`DataGeneratorStrategy`**: Abstract base class
- **Concrete generators**: `NameGenerator`, `EmailGenerator`, `IntegerGenerator`, etc.
- **`DataGeneratorFactory`**: Factory for creating generators

#### File Generators (`src/generators/file_generators.py`)
- **`FileGeneratorStrategy`**: Abstract base class
- **Concrete generators**: `CSVGenerator`, `JSONGenerator`, `XMLGenerator`, etc.
- **`FileGeneratorFactory`**: Factory for creating file generators

#### Services (`src/services/`)
- **`DataGenerationService`**: Main orchestration service
- **Handles**: Configuration validation, batch processing, file generation

#### GUI (`src/gui/`)
- **`MainWindow`**: Main application window
- **Features**: Format selection, dimension configuration, column setup, output configuration

#### CLI (`src/cli/`)
- **`CLIGenerator`**: Command-line interface
- **Features**: Argument parsing, configuration validation, batch processing

## Data Flow

1. **Configuration**: User configures file format, dimensions, and column types
2. **Validation**: Configuration is validated for correctness
3. **Data Generation**: Data is generated in batches using appropriate generators
4. **File Creation**: Generated data is written to file using appropriate format generator
5. **Output**: File is saved to specified location

## Extensibility

### Adding New Data Types
1. Create new class implementing `DataGeneratorStrategy`
2. Add to `DataGeneratorFactory._generators` dictionary
3. Add to `DataType` enum

### Adding New File Formats
1. Create new class implementing `FileGeneratorStrategy`
2. Add to `FileGeneratorFactory._generators` dictionary

### Adding New Features
1. Follow existing patterns and SOLID principles
2. Add appropriate tests
3. Update documentation

## Testing Strategy

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Test Coverage**: Aim for high coverage of business logic
- **Test Data**: Use reproducible seeds for deterministic testing

## Performance Considerations

- **Batch Processing**: Large datasets are processed in configurable batches
- **Memory Management**: Data is generated incrementally to avoid memory issues
- **Efficient I/O**: File writing is optimized for each format
- **Configurable Limits**: Reasonable limits on rows and columns to prevent abuse

