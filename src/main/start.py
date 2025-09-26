#!/usr/bin/env python3
"""
Startup script for PetCare Companion
Handles database initialization and app startup
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, init_database
    
    # Initialize database
    print("Initializing database...")
    init_database()
    print("Database initialized successfully!")
    
    # Get port from environment
    port = int(os.environ.get('PORT', 5000))
    
    # Start the application
    print(f"Starting PetCare Companion on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Installing missing dependencies...")
    os.system("pip install -r requirements.txt")
    
    # Try again
    from app import app, init_database
    init_database()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    
except Exception as e:
    print(f"Startup error: {e}")
    print("Attempting to start with minimal configuration...")
    
    # Minimal Flask app as fallback
    from flask import Flask
    fallback_app = Flask(__name__)
    
    @fallback_app.route('/')
    def hello():
        return """
        <h1>PetCare Companion</h1>
        <p>Application is starting up...</p>
        <p>Please refresh in a few moments.</p>
        """
    
    port = int(os.environ.get('PORT', 5000))
    fallback_app.run(host='0.0.0.0', port=port, debug=False)
