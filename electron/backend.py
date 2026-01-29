#!/usr/bin/env python3
"""
Electron integration launcher
Launches the Flask backend and prepares it for Electron communication
"""
import os
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('TimeMachine-Electron')

def main():
    """Main entry point for Electron backend"""
    logger.info("Starting TimeMachine Electron Backend")
    
    # Add the project root to Python path
    project_root = Path(__file__).parent.parent  # Go up one level to project root
    sys.path.insert(0, str(project_root))
    
    # Import and run the Flask app
    try:
        from app import app, server
        
        logger.info("Starting Flask server on localhost:5000")
        
        # Run Flask in a way that's compatible with Electron
        # Set debug=False for production-like behavior
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False,  # Important: disable reloader in Electron context
            threaded=True
        )
    except ImportError as e:
        logger.error(f"Failed to import app: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
