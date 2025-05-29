import tkinter as tk
from gui import SheetMetalClientHub
from logging_config import setup_logger
import platform
import sys
import logging

# Set up logging
logger = setup_logger('main', 'main.log')

if __name__ == "__main__":
    try:
        logger.info("Starting Sheet Metal Client Hub application")
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Platform: {platform.platform()}")
        root = tk.Tk()
        app = SheetMetalClientHub(root)
        root.mainloop()
    except TypeError as e:
        logger.error(f"Constructor error in SheetMetalClientHub: {e}")
        logger.debug(f"Check gui.py SheetMetalClientHub.__init__ signature. Ensure it accepts 'root' parameter.")
    except AttributeError as e:
        logger.error(f"Missing method in SheetMetalClientHub: {e}")
        logger.debug(f"Verify gui.py contains all required methods (e.g., create_login_screen)")
    except tk.TclError as e:
        logger.error(f"Tkinter error starting GUI: {e}")
    except Exception as e:
        logger.error(f"Unexpected error starting GUI: {e}")
    finally:
        logger.info("Application closed")