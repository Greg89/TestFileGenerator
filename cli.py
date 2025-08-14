#!/usr/bin/env python3
"""
Command-line interface entry point for the Test Data Generator.
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cli.cli_generator import main

if __name__ == "__main__":
    main()
