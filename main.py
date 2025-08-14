#!/usr/bin/env python3
"""
Main entry point for the Test Data Generator application.
"""
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from gui.main_window import MainWindow


def main():
    """Main application entry point."""
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
