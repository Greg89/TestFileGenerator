"""
Data generation strategies following the Strategy Pattern.
Each generator is responsible for a specific data type.
"""
from abc import ABC, abstractmethod
from typing import Any, Optional
from faker import Faker
import random
import uuid
from datetime import datetime, timedelta

from ..models.data_config import DataType, ColumnConfig


class DataGeneratorStrategy(ABC):
    """Abstract base class for data generation strategies."""

    @abstractmethod
    def generate(self, config: ColumnConfig) -> Any:
        """Generate data based on the column configuration."""
        pass


class NameGenerator(DataGeneratorStrategy):
    """Generates realistic names."""

    def __init__(self):
        self.faker = Faker()

    def generate(self, config: ColumnConfig) -> str:
        return self.faker.name()


class EmailGenerator(DataGeneratorStrategy):
    """Generates realistic email addresses."""

    def __init__(self):
        self.faker = Faker()

    def generate(self, config: ColumnConfig) -> str:
        return self.faker.email()


class PhoneGenerator(DataGeneratorStrategy):
    """Generates phone numbers."""

    def __init__(self):
        self.faker = Faker()

    def generate(self, config: ColumnConfig) -> str:
        return self.faker.phone_number()


class AddressGenerator(DataGeneratorStrategy):
    """Generates addresses."""

    def __init__(self):
        self.faker = Faker()

    def generate(self, config: ColumnConfig) -> str:
        return self.faker.address()


class CompanyGenerator(DataGeneratorStrategy):
    """Generates company names."""

    def __init__(self):
        self.faker = Faker()

    def generate(self, config: ColumnConfig) -> str:
        return self.faker.company()


class JobGenerator(DataGeneratorStrategy):
    """Generates job titles."""

    def __init__(self):
        self.faker = Faker()

    def generate(self, config: ColumnConfig) -> str:
        return self.faker.job()


class DateGenerator(DataGeneratorStrategy):
    """Generates dates."""

    def __init__(self):
        self.faker = Faker()

    def generate(self, config: ColumnConfig) -> str:
        return self.faker.date()


class IntegerGenerator(DataGeneratorStrategy):
    """Generates integers within a specified range."""

    def generate(self, config: ColumnConfig) -> int:
        min_val = config.min_value if config.min_value is not None else 0
        max_val = config.max_value if config.max_value is not None else 1000
        return random.randint(int(min_val), int(max_val))


class FloatGenerator(DataGeneratorStrategy):
    """Generates floats within a specified range."""

    def generate(self, config: ColumnConfig) -> float:
        min_val = config.min_value if config.min_value is not None else 0.0
        max_val = config.max_value if config.max_value is not None else 1000.0
        return round(random.uniform(min_val, max_val), 2)


class BooleanGenerator(DataGeneratorStrategy):
    """Generates boolean values."""

    def generate(self, config: ColumnConfig) -> bool:
        return random.choice([True, False])


class TextGenerator(DataGeneratorStrategy):
    """Generates random text."""

    def __init__(self):
        self.faker = Faker()

    def generate(self, config: ColumnConfig) -> str:
        length = config.text_length if config.text_length is not None else 50
        return self.faker.text(max_nb_chars=length)


class URLGenerator(DataGeneratorStrategy):
    """Generates URLs."""

    def __init__(self):
        self.faker = Faker()

    def generate(self, config: ColumnConfig) -> str:
        return self.faker.url()


class IPAddressGenerator(DataGeneratorStrategy):
    """Generates IP addresses."""

    def __init__(self):
        self.faker = Faker()

    def generate(self, config: ColumnConfig) -> str:
        return self.faker.ipv4()


class UUIDGenerator(DataGeneratorStrategy):
    """Generates UUIDs."""

    def generate(self, config: ColumnConfig) -> str:
        return str(uuid.uuid4())


class CreditCardGenerator(DataGeneratorStrategy):
    """Generates credit card numbers."""

    def __init__(self):
        self.faker = Faker()

    def generate(self, config: ColumnConfig) -> str:
        return self.faker.credit_card_number()


class DataGeneratorFactory:
    """Factory for creating data generators following the Factory Pattern."""

    _generators = {
        DataType.NAME: NameGenerator,
        DataType.EMAIL: EmailGenerator,
        DataType.PHONE: PhoneGenerator,
        DataType.ADDRESS: AddressGenerator,
        DataType.COMPANY: CompanyGenerator,
        DataType.JOB: JobGenerator,
        DataType.DATE: DateGenerator,
        DataType.INTEGER: IntegerGenerator,
        DataType.FLOAT: FloatGenerator,
        DataType.BOOLEAN: BooleanGenerator,
        DataType.TEXT: TextGenerator,
        DataType.URL: URLGenerator,
        DataType.IP_ADDRESS: IPAddressGenerator,
        DataType.UUID: UUIDGenerator,
        DataType.CREDIT_CARD: CreditCardGenerator,
    }

    @classmethod
    def create_generator(cls, data_type: DataType) -> DataGeneratorStrategy:
        """Create a generator for the specified data type."""
        if data_type not in cls._generators:
            raise ValueError(f"Unsupported data type: {data_type}")

        generator_class = cls._generators[data_type]
        return generator_class()

    @classmethod
    def get_available_types(cls) -> list[DataType]:
        """Get list of available data types."""
        return list(cls._generators.keys())

