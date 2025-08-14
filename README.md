# Test Data Generator

A professional-grade application for generating test documents in various formats (CSV, TXT, XML, JSON, EXCEL) with configurable parameters and truly random data.

## Features

- **Multiple File Formats**: Generate CSV, TXT, XML, JSON, and Excel files
- **Configurable Parameters**: Set number of rows, columns, and data types
- **Random Data Generation**: Uses Faker library for realistic, varied datasets
- **Clean Architecture**: Follows SOLID principles and industry standards
- **Modern GUI**: Intuitive interface for easy configuration and generation

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Select the desired file format
2. Configure the number of rows and columns
3. Choose data types for each column
4. Set output directory and filename
5. Click "Generate" to create your test file

## Architecture

- **Command Pattern**: For file generation operations
- **Factory Pattern**: For creating different file format generators
- **Strategy Pattern**: For different data generation strategies
- **SOLID Principles**: Clean, maintainable, and extensible code

## Supported Formats

- **CSV**: Comma-separated values with configurable delimiters
- **JSON**: Structured data with nested objects and arrays
- **XML**: Hierarchical data with custom element names
- **TXT**: Plain text with various formatting options
- **EXCEL**: Spreadsheet format with multiple sheets support

