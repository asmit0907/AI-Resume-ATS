# run_app.py
import os
import sys
import streamlit.web.cli as stcli

def resolve_path(relative_path):
    """Handles asset path resolution for compiled PyInstaller binaries."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if __name__ == "__main__":
    # Ensure Streamlit points to your app file location
    script_path = resolve_path("app.py")
    
    sys.argv = [
        "streamlit",
        "run",
        script_path,
        "--global.developmentMode=false"
    ]
    
    sys.exit(stcli.main())