#!/usr/bin/env python3
"""
Example script demonstrating programmatic usage of the Test Data Generator.
This shows how to use the library in your own Python scripts.
"""
import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.data_config import FileConfig, ColumnConfig, DataType, GenerationRequest
from services.data_generation_service import DataGenerationService


def generate_user_dataset():
    """Generate a sample user dataset with realistic data."""
    print("Generating user dataset...")

    # Configure columns for user data
    columns = [
        ColumnConfig(name="user_id", data_type=DataType.UUID),
        ColumnConfig(name="first_name", data_type=DataType.NAME),
        ColumnConfig(name="last_name", data_type=DataType.NAME),
        ColumnConfig(name="email", data_type=DataType.EMAIL),
        ColumnConfig(name="phone", data_type=DataType.PHONE),
        ColumnConfig(name="company", data_type=DataType.COMPANY),
        ColumnConfig(name="job_title", data_type=DataType.JOB),
        ColumnConfig(name="age", data_type=DataType.INTEGER, min_value=18, max_value=80),
        ColumnConfig(name="salary", data_type=DataType.FLOAT, min_value=30000, max_value=200000),
        ColumnConfig(name="is_active", data_type=DataType.BOOLEAN)
    ]

    # Create file configuration
    file_config = FileConfig(
        file_format="csv",
        num_rows=1000,
        num_columns=10,
        columns=columns,
        output_path="examples/output/users.csv"
    )

    # Create generation request
    request = GenerationRequest(
        config=file_config,
        seed=42,  # Fixed seed for reproducible results
        batch_size=1000
    )

    # Generate data
    service = DataGenerationService()
    output_file = service.generate_test_data(request)

    print(f"Generated user dataset: {output_file}")
    return output_file


def generate_product_dataset():
    """Generate a sample product dataset."""
    print("Generating product dataset...")

    columns = [
        ColumnConfig(name="product_id", data_type=DataType.UUID),
        ColumnConfig(name="product_name", data_type=DataType.TEXT, text_length=50),
        ColumnConfig(name="category", data_type=DataType.TEXT, text_length=30),
        ColumnConfig(name="price", data_type=DataType.FLOAT, min_value=0.99, max_value=999.99),
        ColumnConfig(name="stock_quantity", data_type=DataType.INTEGER, min_value=0, max_value=1000),
        ColumnConfig(name="rating", data_type=DataType.FLOAT, min_value=1.0, max_value=5.0),
        ColumnConfig(name="is_available", data_type=DataType.BOOLEAN),
        ColumnConfig(name="website", data_type=DataType.URL)
    ]

    file_config = FileConfig(
        file_format="json",
        num_rows=500,
        num_columns=8,
        columns=columns,
        output_path="examples/output/products.json"
    )

    request = GenerationRequest(
        config=file_config,
        seed=None,  # Random seed for variety
        batch_size=500
    )

    service = DataGenerationService()
    output_file = service.generate_test_data(request)

    print(f"Generated product dataset: {output_file}")
    return output_file


def generate_sales_dataset():
    """Generate a sample sales dataset."""
    print("Generating sales dataset...")

    columns = [
        ColumnConfig(name="transaction_id", data_type=DataType.UUID),
        ColumnConfig(name="customer_name", data_type=DataType.NAME),
        ColumnConfig(name="product_name", data_type=DataType.TEXT, text_length=40),
        ColumnConfig(name="quantity", data_type=DataType.INTEGER, min_value=1, max_value=100),
        ColumnConfig(name="unit_price", data_type=DataType.FLOAT, min_value=1.0, max_value=500.0),
        ColumnConfig(name="total_amount", data_type=DataType.FLOAT, min_value=1.0, max_value=50000.0),
        ColumnConfig(name="sale_date", data_type=DataType.DATE),
        ColumnConfig(name="payment_method", data_type=DataType.TEXT, text_length=20),
        ColumnConfig(name="customer_email", data_type=DataType.EMAIL),
        ColumnConfig(name="ip_address", data_type=DataType.IP_ADDRESS)
    ]

    file_config = FileConfig(
        file_format="excel",
        num_rows=2000,
        num_columns=10,
        columns=columns,
        output_path="examples/output/sales.xlsx"
    )

    request = GenerationRequest(
        config=file_config,
        seed=123,
        batch_size=1000
    )

    service = DataGenerationService()
    output_file = service.generate_test_data(request)

    print(f"Generated sales dataset: {output_file}")
    return output_file


def generate_log_dataset():
    """Generate a sample log dataset."""
    print("Generating log dataset...")

    columns = [
        ColumnConfig(name="timestamp", data_type=DataType.DATE),
        ColumnConfig(name="log_level", data_type=DataType.TEXT, text_length=10),
        ColumnConfig(name="service_name", data_type=DataType.TEXT, text_length=30),
        ColumnConfig(name="message", data_type=DataType.TEXT, text_length=200),
        ColumnConfig(name="user_id", data_type=DataType.UUID),
        ColumnConfig(name="ip_address", data_type=DataType.IP_ADDRESS),
        ColumnConfig(name="response_time", data_type=DataType.FLOAT, min_value=0.001, max_value=10.0),
        ColumnConfig(name="status_code", data_type=DataType.INTEGER, min_value=200, max_value=599)
    ]

    file_config = FileConfig(
        file_format="xml",
        num_rows=10000,
        num_columns=8,
        columns=columns,
        output_path="examples/output/application_logs.xml"
    )

    request = GenerationRequest(
        config=file_config,
        seed=456,
        batch_size=2000
    )

    service = DataGenerationService()
    output_file = service.generate_test_data(request)

    print(f"Generated log dataset: {output_file}")
    return output_file


def main():
    """Main function to generate all sample datasets."""
    print("Test Data Generator - Example Script")
    print("=" * 50)

    # Create output directory
    output_dir = Path("examples/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Generate different types of datasets
        files = []

        files.append(generate_user_dataset())
        files.append(generate_product_dataset())
        files.append(generate_sales_dataset())
        files.append(generate_log_dataset())

        print("\n" + "=" * 50)
        print("All datasets generated successfully!")
        print("\nGenerated files:")
        for file_path in files:
            file_size = Path(file_path).stat().st_size
            print(f"  - {file_path} ({file_size:,} bytes)")

        print(f"\nFiles saved to: {output_dir.absolute()}")

    except Exception as e:
        print(f"Error generating datasets: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

