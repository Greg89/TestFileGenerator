"""
Unit tests for data generators.
"""
import unittest
from unittest.mock import Mock
import random

from src.generators.data_generator import (
    DataGeneratorFactory, NameGenerator, EmailGenerator,
    IntegerGenerator, FloatGenerator, BooleanGenerator
)
from src.models.data_config import DataType, ColumnConfig


class TestDataGenerators(unittest.TestCase):
    """Test cases for data generators."""

    def setUp(self):
        """Set up test fixtures."""
        # Set random seed for reproducible tests
        random.seed(42)

    def test_name_generator(self):
        """Test name generation."""
        generator = NameGenerator()
        config = ColumnConfig(name="test", data_type=DataType.NAME)

        name = generator.generate(config)
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)

    def test_email_generator(self):
        """Test email generation."""
        generator = EmailGenerator()
        config = ColumnConfig(name="test", data_type=DataType.EMAIL)

        email = generator.generate(config)
        self.assertIsInstance(email, str)
        self.assertIn('@', email)
        self.assertIn('.', email)

    def test_integer_generator_default_range(self):
        """Test integer generation with default range."""
        generator = IntegerGenerator()
        config = ColumnConfig(name="test", data_type=DataType.INTEGER)

        value = generator.generate(config)
        self.assertIsInstance(value, int)
        self.assertTrue(0 <= value <= 1000)

    def test_integer_generator_custom_range(self):
        """Test integer generation with custom range."""
        generator = IntegerGenerator()
        config = ColumnConfig(
            name="test",
            data_type=DataType.INTEGER,
            min_value=10,
            max_value=20
        )

        value = generator.generate(config)
        self.assertIsInstance(value, int)
        self.assertTrue(10 <= value <= 20)

    def test_float_generator_default_range(self):
        """Test float generation with default range."""
        generator = FloatGenerator()
        config = ColumnConfig(name="test", data_type=DataType.FLOAT)

        value = generator.generate(config)
        self.assertIsInstance(value, float)
        self.assertTrue(0.0 <= value <= 1000.0)

    def test_float_generator_custom_range(self):
        """Test float generation with custom range."""
        generator = FloatGenerator()
        config = ColumnConfig(
            name="test",
            data_type=DataType.FLOAT,
            min_value=1.5,
            max_value=2.5
        )

        value = generator.generate(config)
        self.assertIsInstance(value, float)
        self.assertTrue(1.5 <= value <= 2.5)

    def test_boolean_generator(self):
        """Test boolean generation."""
        generator = BooleanGenerator()
        config = ColumnConfig(name="test", data_type=DataType.BOOLEAN)

        values = [generator.generate(config) for _ in range(100)]
        self.assertTrue(any(values))  # At least one True
        self.assertTrue(not all(values))  # At least one False

    def test_factory_creates_generators(self):
        """Test that factory creates correct generators."""
        factory = DataGeneratorFactory()

        # Test all data types
        for data_type in DataType:
            generator = factory.create_generator(data_type)
            self.assertIsNotNone(generator)

    def test_factory_invalid_type(self):
        """Test factory with invalid data type."""
        factory = DataGeneratorFactory()

        with self.assertRaises(ValueError):
            factory.create_generator("invalid_type")

    def test_factory_available_types(self):
        """Test that factory returns all available types."""
        factory = DataGeneratorFactory()
        available_types = factory.get_available_types()

        self.assertEqual(len(available_types), len(DataType))
        for data_type in DataType:
            self.assertIn(data_type, available_types)


if __name__ == '__main__':
    unittest.main()
