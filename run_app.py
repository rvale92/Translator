"""Entry point for the Voice Translation App."""
import os
import sys
from pathlib import Path
import streamlit.web.bootstrap as bootstrap
from flask import Flask, jsonify
from dotenv import load_dotenv

app = Flask(__name__, static_folder='.', static_url_path='')
load_dotenv()

@app.route('/api/config')
def get_config():
    return jsonify({
        'apiKey': os.getenv('OPENAI_API_KEY')
    })

def run():
    """Run the Streamlit app."""
    # Add the project root to Python path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # Get the main app path
    main_app_path = str(project_root / "app" / "main.py")
    
    # Get port from environment variable (for Render compatibility)
    port = int(os.environ.get("PORT", 8501))
    
    # Run the Streamlit app using the bootstrap module
    flag_options = {
        "server.port": port,
        "server.address": "0.0.0.0",
        "server.headless": True,
        "server.enableCORS": False,
        "server.enableXsrfProtection": False
    }
    
    bootstrap.run(main_app_path, "", flag_options)

if __name__ == '__main__':
    app.run(debug=True, port=8000) 