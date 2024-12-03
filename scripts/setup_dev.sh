#!/bin/bash

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install development dependencies
pip install -e .
pip install pytest pytest-mock pytest-cov pylint black

# Create necessary directories
mkdir -p reports
mkdir -p logs

# Setup pre-commit hooks
cp scripts/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit

echo "Development environment setup complete!"