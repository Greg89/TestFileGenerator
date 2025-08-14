"""
File format generators following the Strategy Pattern.
Each generator handles a specific file format output.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import csv
import json
import xml.etree.ElementTree as ET
import pandas as pd
from pathlib import Path

from ..models.data_config import FileConfig, ColumnConfig
from .data_generator import DataGeneratorFactory


class FileGeneratorStrategy(ABC):
    """Abstract base class for file generation strategies."""

    @abstractmethod
    def generate(self, config: FileConfig, data: List[Dict[str, Any]]) -> None:
        """Generate file with the specified format."""
        pass


class CSVGenerator(FileGeneratorStrategy):
    """Generates CSV files."""

    def generate(self, config: FileConfig, data: List[Dict[str, Any]]) -> None:
        """Generate CSV file from data."""
        if not data:
            raise ValueError("No data provided for CSV generation")

        with open(config.output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [col.name for col in config.columns]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in data:
                writer.writerow(row)


class JSONGenerator(FileGeneratorStrategy):
    """Generates JSON files."""

    def generate(self, config: FileConfig, data: List[Dict[str, Any]]) -> None:
        """Generate JSON file from data."""
        if not data:
            raise ValueError("No data provided for JSON generation")

        with open(config.output_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)


class XMLGenerator(FileGeneratorStrategy):
    """Generates XML files."""

    def generate(self, config: FileConfig, data: List[Dict[str, Any]]) -> None:
        """Generate XML file from data."""
        if not data:
            raise ValueError("No data provided for XML generation")

        root = ET.Element("data")

        for row in data:
            record = ET.SubElement(root, "record")
            for col in config.columns:
                element = ET.SubElement(record, col.name)
                element.text = str(row.get(col.name, ""))

        tree = ET.ElementTree(root)
        tree.write(config.output_path, encoding='utf-8', xml_declaration=True)


class TXTGenerator(FileGeneratorStrategy):
    """Generates plain text files."""

    def generate(self, config: FileConfig, data: List[Dict[str, Any]]) -> None:
        """Generate TXT file from data."""
        if not data:
            raise ValueError("No data provided for TXT generation")

        with open(config.output_path, 'w', encoding='utf-8') as txtfile:
            # Write header
            header = " | ".join(col.name for col in config.columns)
            txtfile.write(header + "\n")
            txtfile.write("-" * len(header) + "\n")

            # Write data rows
            for row in data:
                row_data = " | ".join(str(row.get(col.name, "")) for col in config.columns)
                txtfile.write(row_data + "\n")


class ExcelGenerator(FileGeneratorStrategy):
    """Generates Excel files."""

    def generate(self, config: FileConfig, data: List[Dict[str, Any]]) -> None:
        """Generate Excel file from data."""
        if not data:
            raise ValueError("No data provided for Excel generation")

        df = pd.DataFrame(data)
        df.to_excel(config.output_path, index=False, sheet_name='Sheet1')


class FileGeneratorFactory:
    """Factory for creating file generators following the Factory Pattern."""

    _generators = {
        "csv": CSVGenerator,
        "json": JSONGenerator,
        "xml": XMLGenerator,
        "txt": TXTGenerator,
        "excel": ExcelGenerator,
    }

    @classmethod
    def create_generator(cls, file_format: str) -> FileGeneratorStrategy:
        """Create a generator for the specified file format."""
        if file_format not in cls._generators:
            raise ValueError(f"Unsupported file format: {file_format}")

        generator_class = cls._generators[file_format]
        return generator_class()

    @classmethod
    def get_available_formats(cls) -> list[str]:
        """Get list of available file formats."""
        return list(cls._generators.keys())

