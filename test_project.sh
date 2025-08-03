#!/bin/bash
# Pet Care Project Health Check Script for Linux/Mac
# This script tests if the project is running correctly

echo ""
echo "========================================"
echo "🐾 Pet Care Project Health Check"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python is not installed or not in PATH"
        echo "Please install Python and try again"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python found: $($PYTHON_CMD --version)"

# Check if requests library is available
$PYTHON_CMD -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installing required library: requests"
    $PYTHON_CMD -m pip install requests
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install requests library"
        echo "Try: pip3 install requests"
        exit 1
    fi
fi

# Run the health check tests
echo "🔍 Running health check tests..."
echo ""

$PYTHON_CMD project_health_tests.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Some tests failed. Please check the output above."
    echo ""
    echo "💡 Common solutions:"
    echo "   1. Make sure Flask app is running: python app.py"
    echo "   2. Check if all dependencies are installed: pip install -r requirements.txt"
    echo "   3. Verify database is initialized"
    echo ""
    exit 1
else
    echo ""
    echo "✅ All tests passed! Your project is running correctly."
    echo ""
fi
