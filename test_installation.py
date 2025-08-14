#!/usr/bin/env python3
"""
Test script to verify the Test Data Generator installation.
This script checks that all dependencies are available and basic functionality works.
"""
import sys
import os

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")

    try:
        # Test basic Python modules
        import csv
        import json
        import xml.etree.ElementTree
        import pandas
        print("✓ Basic Python modules imported successfully")

        # Test third-party packages
        import faker
        import pydantic
        print("✓ Third-party packages imported successfully")

        # Test our modules
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

        from models.data_config import DataType, ColumnConfig, FileConfig
        from generators.data_generator import DataGeneratorFactory
        from generators.file_generators import FileGeneratorFactory
        from services.data_generation_service import DataGenerationService
        print("✓ Application modules imported successfully")

        return True

    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during import: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without generating files."""
    print("\nTesting basic functionality...")

    try:
        from models.data_config import DataType, ColumnConfig, FileConfig
        from generators.data_generator import DataGeneratorFactory
        from generators.file_generators import FileGeneratorFactory
        from services.data_generation_service import DataGenerationService

        # Test data type factory
        factory = DataGeneratorFactory()
        available_types = factory.get_available_types()
        print(f"✓ Available data types: {len(available_types)}")

        # Test file format factory
        file_factory = FileGeneratorFactory()
        available_formats = file_factory.get_available_formats()
        print(f"✓ Available file formats: {available_formats}")

        # Test service creation
        service = DataGenerationService()
        print("✓ Data generation service created successfully")

        return True

    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False

def test_simple_generation():
    """Test simple data generation without file output."""
    print("\nTesting simple data generation...")

    try:
        from models.data_config import DataType, ColumnConfig, FileConfig
        from generators.data_generator import DataGeneratorFactory

        # Create a simple column configuration
        column = ColumnConfig(
            name="test_column",
            data_type=DataType.NAME
        )

        # Test data generation
        factory = DataGeneratorFactory()
        generator = factory.create_generator(DataType.NAME)
        data = generator.generate(column)

        print(f"✓ Generated test data: {data}")
        return True

    except Exception as e:
        print(f"✗ Data generation test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Test Data Generator - Installation Test")
    print("=" * 50)

    tests = [
        ("Import Test", test_imports),
        ("Basic Functionality Test", test_basic_functionality),
        ("Data Generation Test", test_simple_generation)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
            print(f"✓ {test_name} PASSED")
        else:
            print(f"✗ {test_name} FAILED")

    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The Test Data Generator is ready to use.")
        print("\nYou can now run:")
        print("  python main.py          # Launch GUI application")
        print("  python cli.py --help    # View CLI options")
        print("  python examples/generate_sample_data.py  # Run examples")
        return 0
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
