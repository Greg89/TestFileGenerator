"""
Data generation service that orchestrates the entire generation process.
Follows Single Responsibility Principle by handling only the orchestration logic.
"""
import random
from typing import List, Dict, Any
from pathlib import Path

from ..models.data_config import GenerationRequest, FileConfig, ColumnConfig
from ..generators.data_generator import DataGeneratorFactory
from ..generators.file_generators import FileGeneratorFactory


class DataGenerationService:
    """Main service for orchestrating data generation and file creation."""

    def __init__(self):
        self.data_generator_factory = DataGeneratorFactory()
        self.file_generator_factory = FileGeneratorFactory()

    def generate_test_data(self, request: GenerationRequest) -> str:
        """
        Generate test data and save it to the specified file format.

        Args:
            request: Complete generation request with configuration

        Returns:
            Path to the generated file

        Raises:
            ValueError: If configuration is invalid
            RuntimeError: If generation fails
        """
        try:
            # Set random seed if provided
            if request.seed is not None:
                random.seed(request.seed)

            # Validate output directory
            output_path = Path(request.config.output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Generate data in batches for memory efficiency
            all_data = []
            for batch_start in range(0, request.config.num_rows, request.batch_size):
                batch_end = min(batch_start + request.batch_size, request.config.num_rows)
                batch_data = self._generate_batch(request.config, batch_start, batch_end)
                all_data.extend(batch_data)

            # Generate file using appropriate format generator
            file_generator = self.file_generator_factory.create_generator(
                request.config.file_format
            )
            file_generator.generate(request.config, all_data)

            return str(output_path)

        except Exception as e:
            raise RuntimeError(f"Data generation failed: {str(e)}") from e

    def _generate_batch(self, config: FileConfig, start_row: int, end_row: int) -> List[Dict[str, Any]]:
        """
        Generate a batch of data rows.

        Args:
            config: File configuration
            start_row: Starting row index
            end_row: Ending row index

        Returns:
            List of data dictionaries
        """
        batch_data = []

        for row_num in range(start_row, end_row):
            row_data = {}

            for col in config.columns:
                # Create data generator for this column type
                data_generator = self.data_generator_factory.create_generator(col.data_type)

                # Generate data for this column
                row_data[col.name] = data_generator.generate(col)

            batch_data.append(row_data)

        return batch_data

    def get_available_data_types(self) -> List[str]:
        """Get list of available data types."""
        return [dt.value for dt in self.data_generator_factory.get_available_types()]

    def get_available_file_formats(self) -> List[str]:
        """Get list of available file formats."""
        return self.file_generator_factory.get_available_formats()

    def validate_configuration(self, config: FileConfig) -> List[str]:
        """
        Validate configuration and return list of errors.

        Args:
            config: File configuration to validate

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        try:
            # Validate using Pydantic
            config.model_validate(config.model_dump())
        except Exception as e:
            errors.append(f"Configuration validation failed: {str(e)}")

        # Additional business logic validation
        if config.num_rows > 1000000:
            errors.append("Number of rows cannot exceed 1,000,000")

        if config.num_columns > 100:
            errors.append("Number of columns cannot exceed 100")

        # Validate output path
        try:
            output_path = Path(config.output_path)
            if output_path.suffix.lower() != f".{config.file_format}":
                errors.append(f"Output file extension should match format: .{config.file_format}")
        except Exception as e:
            errors.append(f"Invalid output path: {str(e)}")

        return errors

