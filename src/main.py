import sys
import os
import tkinter as tk
import logging

# Add the parent directory (src/) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set up logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'data', 'log')
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'main.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:
    from gui import SheetMetalClientHub
except ImportError as e:
    logging.error(f"Failed to import SheetMetalClientHub: {e}")
    print(f"Error: Failed to import SheetMetalClientHub: {e}")
    sys.exit(1)

def main():
    """Launch the Sheet Metal Client Hub GUI."""
    logging.info("Starting Sheet Metal Client Hub application")
    try:
        root = tk.Tk()
        app = SheetMetalClientHub(root)
        root.mainloop()
        logging.info("Application closed successfully")
    except Exception as e:
        logging.error(f"Error launching GUI: {e}")
        print(f"Error launching GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()