# main.py
# Purpose: Entry point for the Sheet Metal Client Hub application.
# Initializes the Tkinter GUI and starts the application.
# Integrates all modules (gui.py, calculator.py, file_handler.py) to provide functionality for FR1-FR7.
# Minimal code to keep the entry point clean and focused on starting the GUI.

from gui import SheetMetalClientHub
import tkinter as tk
import logging

# Set up logging
logging.basicConfig(filename='main_output.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def main():
    """
    Main function to start the Sheet Metal Client Hub application.

    Logic:
        1. Creates a Tkinter root window.
        2. Instantiates the SheetMetalClientHub GUI class.
        3. Starts the Tkinter main event loop to display the GUI.
    """
    try:
        root = tk.Tk()
        app = SheetMetalClientHub(root)
        logging.info("GUI launched successfully")
        root.mainloop()
    except Exception as e:
        logging.error(f"Error launching GUI: {e}")
        raise

if __name__ == "__main__":
    # Entry point check to ensure main() is called only when the script is run directly
    main()
