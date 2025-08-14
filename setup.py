from setuptools import setup, find_packages

setup(
    name="test-data-generator",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)

