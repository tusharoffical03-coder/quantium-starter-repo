#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Activating virtual environment..."
source venv/Scripts/activate

echo "Running test suite..."
python -m pytest

echo "All tests passed successfully!"
exit 0
