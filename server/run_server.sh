#!/bin/bash
# Helper script to run the FastAPI server with proper environment setup

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the backend directory
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

echo "🚀 Starting Carely AI Backend Server..."
echo "📖 API Documentation: http://localhost:8000/docs"
echo "🔧 Alternative Docs: http://localhost:8000/redoc"
echo ""

# Run uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000



