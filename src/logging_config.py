import logging
import os

def setup_logger(name, log_file):
    """
    Configure a logger with file and console handlers.
    Args:
        name: Logger name (e.g., 'gui', 'utils').
        log_file: Path to log file (e.g., 'data/log/gui.log').
    Returns:
        Configured logger instance.
    """
    LOG_DIR = r"C:\Users\Laurie\Proton Drive\tartant\My files\GitHub\Sheet-Metal-Client-Hub\data\log"
    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, log_file)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(log_path, mode='a')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(console_handler)

        logger.info(f"{name} logging initialized")
        file_handler.flush()

    return logger