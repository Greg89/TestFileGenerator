"""
Command-line interface for the Test Data Generator.
Provides an alternative to the GUI for automation and scripting.
"""
import argparse
import sys
from pathlib import Path
from typing import List

from ..models.data_config import FileConfig, ColumnConfig, DataType, GenerationRequest
from ..services.data_generation_service import DataGenerationService


class CLIGenerator:
    """Command-line interface for test data generation."""

    def __init__(self):
        self.service = DataGenerationService()
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create command-line argument parser."""
        parser = argparse.ArgumentParser(
            description="Generate test data files in various formats",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Generate CSV with 100 rows, 5 columns
  python cli_generator.py --format csv --rows 100 --columns 5 --output test.csv

  # Generate JSON with custom column types
  python cli_generator.py --format json --rows 50 --columns 3 \\
    --column-types name,email,phone --output users.json

  # Generate Excel with specific data ranges
  python cli_generator.py --format excel --rows 1000 --columns 4 \\
    --column-types integer,float,boolean,text \\
    --min-values 0,0.0,None,None \\
    --max-values 100,1000.0,None,None \\
    --output data.xlsx
            """
        )

        # Basic options
        parser.add_argument(
            '--format', '-f',
            choices=self.service.get_available_file_formats(),
            default='csv',
            help='Output file format (default: csv)'
        )

        parser.add_argument(
            '--rows', '-r',
            type=int,
            default=100,
            help='Number of rows to generate (default: 100)'
        )

        parser.add_argument(
            '--columns', '-c',
            type=int,
            default=5,
            help='Number of columns to generate (default: 5)'
        )

        parser.add_argument(
            '--output', '-o',
            required=True,
            help='Output file path'
        )

        # Column configuration
        parser.add_argument(
            '--column-types',
            nargs='+',
            help='Data types for columns (e.g., name email phone)'
        )

        parser.add_argument(
            '--column-names',
            nargs='+',
            help='Names for columns (e.g., id name email)'
        )

        parser.add_argument(
            '--min-values',
            nargs='+',
            help='Minimum values for numeric columns'
        )

        parser.add_argument(
            '--max-values',
            nargs='+',
            help='Maximum values for numeric columns'
        )

        parser.add_argument(
            '--text-lengths',
            nargs='+',
            help='Text lengths for text columns'
        )

        # Advanced options
        parser.add_argument(
            '--seed',
            type=int,
            help='Random seed for reproducible results'
        )

        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='Batch size for large datasets (default: 1000)'
        )

        parser.add_argument(
            '--validate-only',
            action='store_true',
            help='Only validate configuration without generating data'
        )

        return parser

    def _parse_column_types(self, types_str: List[str]) -> List[DataType]:
        """Parse column types from command line arguments."""
        if not types_str:
            # Default types
            return [DataType.NAME, DataType.EMAIL, DataType.PHONE, DataType.COMPANY, DataType.JOB][:self.args.columns]

        types = []
        for type_str in types_str:
            try:
                types.append(DataType(type_str.lower()))
            except ValueError:
                print(f"Error: Invalid data type '{type_str}'")
                print(f"Available types: {', '.join(dt.value for dt in DataType)}")
                sys.exit(1)

        return types

    def _parse_numeric_values(self, values_str: List[str]) -> List[float]:
        """Parse numeric values from command line arguments."""
        if not values_str:
            return [None] * self.args.columns

        values = []
        for val_str in values_str:
            if val_str.lower() == 'none':
                values.append(None)
            else:
                try:
                    values.append(float(val_str))
                except ValueError:
                    print(f"Error: Invalid numeric value '{val_str}'")
                    sys.exit(1)

        return values

    def _parse_text_lengths(self, lengths_str: List[str]) -> List[int]:
        """Parse text lengths from command line arguments."""
        if not lengths_str:
            return [None] * self.args.columns

        lengths = []
        for len_str in lengths_str:
            if len_str.lower() == 'none':
                lengths.append(None)
            else:
                try:
                    lengths.append(int(len_str))
                except ValueError:
                    print(f"Error: Invalid text length '{len_str}'")
                    sys.exit(1)

        return lengths

    def _create_column_configs(self) -> List[ColumnConfig]:
        """Create column configurations from command line arguments."""
        column_types = self._parse_column_types(self.args.column_types)
        column_names = self.args.column_names or [f"Column_{i+1}" for i in range(self.args.columns)]
        min_values = self._parse_numeric_values(self.args.min_values)
        max_values = self._parse_numeric_values(self.args.max_values)
        text_lengths = self._parse_text_lengths(self.args.text_lengths)

        # Ensure all lists have the same length
        max_len = max(len(column_types), len(column_names), len(min_values), len(max_values), len(text_lengths))

        column_types = (column_types * (max_len // len(column_types) + 1))[:max_len]
        column_names = (column_names * (max_len // len(column_names) + 1))[:max_len]
        min_values = (min_values * (max_len // len(min_values) + 1))[:max_len]
        max_values = (max_values * (max_len // len(max_values) + 1))[:max_len]
        text_lengths = (text_lengths * (max_len // len(text_lengths) + 1))[:max_len]

        configs = []
        for i in range(self.args.columns):
            config = ColumnConfig(
                name=column_names[i],
                data_type=column_types[i],
                min_value=min_values[i],
                max_value=max_values[i],
                text_length=text_lengths[i]
            )
            configs.append(config)

        return configs

    def run(self, args: List[str] = None) -> int:
        """Run the CLI application."""
        self.args = self.parser.parse_args(args)

        try:
            # Validate basic parameters
            if self.args.rows <= 0:
                print("Error: Number of rows must be positive")
                return 1

            if self.args.columns <= 0:
                print("Error: Number of columns must be positive")
                return 1

            if self.args.rows > 1000000:
                print("Error: Number of rows cannot exceed 1,000,000")
                return 1

            if self.args.columns > 100:
                print("Error: Number of columns cannot exceed 100")
                return 1

            # Create column configurations
            columns = self._create_column_configs()

            # Ensure output file has correct extension
            output_path = self.args.output
            if not output_path.endswith(f".{self.args.format}"):
                output_path = f"{output_path}.{self.args.format}"

            # Create file configuration
            file_config = FileConfig(
                file_format=self.args.format,
                num_rows=self.args.rows,
                num_columns=self.args.columns,
                columns=columns,
                output_path=output_path
            )

            # Validate configuration
            print("Validating configuration...")
            errors = self.service.validate_configuration(file_config)
            if errors:
                print("Configuration errors:")
                for error in errors:
                    print(f"  - {error}")
                return 1

            if self.args.validate_only:
                print("Configuration is valid!")
                return 0

            # Create generation request
            request = GenerationRequest(
                config=file_config,
                seed=self.args.seed,
                batch_size=self.args.batch_size
            )

            # Generate data
            print(f"Generating {self.args.rows} rows with {self.args.columns} columns...")
            print(f"Format: {self.args.format.upper()}")
            print(f"Output: {output_path}")

            output_file = self.service.generate_test_data(request)

            print(f"\nSuccessfully generated: {output_file}")
            print(f"File size: {Path(output_file).stat().st_size:,} bytes")

            return 0

        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 1


def main():
    """CLI entry point."""
    cli = CLIGenerator()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()

