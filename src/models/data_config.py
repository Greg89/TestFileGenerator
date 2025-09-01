"""
Data configuration models for test data generation.
Follows Single Responsibility Principle by handling only configuration concerns.
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class DataType(str, Enum):
    """Available data types for column generation."""
    NAME = "name"
    EMAIL = "email"
    PHONE = "phone"
    ADDRESS = "address"
    COMPANY = "company"
    JOB = "job"
    DATE = "date"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    TEXT = "text"
    URL = "url"
    IP_ADDRESS = "ip_address"
    UUID = "uuid"
    CREDIT_CARD = "credit_card"


class ColumnConfig(BaseModel):
    """Configuration for a single column."""
    name: str = Field(..., description="Column name")
    data_type: DataType = Field(..., description="Type of data to generate")
    min_value: Optional[float] = Field(None, description="Minimum value for numeric types")
    max_value: Optional[float] = Field(None, description="Maximum value for numeric types")
    text_length: Optional[int] = Field(None, description="Length for text fields")

    @field_validator('text_length')
    @classmethod
    def validate_text_length(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Text length must be positive')
        return v

    @field_validator('min_value', 'max_value')
    @classmethod
    def validate_numeric_range(cls, v, info):
        # Note: Pydantic v2 changed the signature - 'values' is now 'info.data'
        if v is not None and info.data:
            if 'min_value' in info.data and 'max_value' in info.data:
                min_val = info.data.get('min_value')
                max_val = info.data.get('max_value')
                if min_val is not None and max_val is not None and min_val >= max_val:
                    raise ValueError('min_value must be less than max_value')
        return v


class FileConfig(BaseModel):
    """Configuration for file generation."""
    file_format: Literal["csv", "json", "xml", "txt", "excel"] = Field(..., description="Output file format")
    num_rows: int = Field(..., ge=1, le=1000000, description="Number of rows to generate")
    num_columns: int = Field(..., ge=1, le=100, description="Number of columns to generate")
    columns: List[ColumnConfig] = Field(..., description="Column configurations")
    output_path: str = Field(..., description="Output file path")

    @field_validator('columns')
    @classmethod
    def validate_columns_match_count(cls, v, info):
        if info.data and 'num_columns' in info.data:
            if len(v) != info.data['num_columns']:
                raise ValueError(f'Number of columns ({len(v)}) must match num_columns ({info.data["num_columns"]})')
        return v

    @field_validator('output_path')
    @classmethod
    def validate_output_path(cls, v):
        if not v.strip():
            raise ValueError('Output path cannot be empty')
        return v


class GenerationRequest(BaseModel):
    """Complete request for data generation."""
    config: FileConfig
    seed: Optional[int] = Field(None, description="Random seed for reproducible results")
    batch_size: int = Field(1000, ge=100, le=10000, description="Batch size for large datasets")

