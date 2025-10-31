#!/bin/bash
# Helper script to run tests with proper environment setup

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the backend directory
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

# Run the quick test
python quick_test.py



