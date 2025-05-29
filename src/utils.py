import hashlib
import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger = logging.getLogger('utils')

def hash_password(password):
    try:
        cleaned_password = str(password).strip()
        if not cleaned_password:
            logger.error("Empty password after cleaning")
            return None
        password_bytes = cleaned_password.encode('utf-8', errors='strict')
        logger.debug(f"Password bytes: {password_bytes!r}")
        hasher = hashlib.sha256()
        hasher.update(password_bytes)
        hashed = hasher.hexdigest()
        logger.debug(f"Generated hash: {hashed} (input: '{cleaned_password}')")
        return hashed
    except UnicodeEncodeError as e:
        logger.error(f"Encoding error in password hashing: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in password hashing: {e}")
        return None

def load_existing_parts():
    try:
        parts_file = os.path.join(BASE_DIR, 'data', 'output.txt')
        parts = []
        with open(parts_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    part_id = line.strip().split(',')[0]
                    parts.append(part_id)
        logger.debug(f"Loaded {len(parts)} parts from {parts_file}")
        return parts
    except FileNotFoundError:
        logger.error(f"Parts file not found: {parts_file}")
        return []
    except Exception as e:
        logger.error(f"Error loading parts: {e}")
        return []

def load_parts_catalogue():
    try:
        catalogue_file = os.path.join(BASE_DIR, 'data', 'parts_catalogue.txt')
        items = []
        with open(catalogue_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) >= 3:
                        item_id, desc, price = parts[0], parts[1], parts[2]
                        try:
                            price = float(price)
                            items.append((item_id, desc, price))
                        except ValueError:
                            logger.warning(f"Invalid price format for {item_id}: {price}")
                            continue
                    else:
                        logger.warning(f"Invalid line format: {line.strip()}")
        logger.debug(f"Loaded {len(items)} items from {catalogue_file}")
        return items
    except FileNotFoundError:
        logger.error(f"Catalogue file not found: {catalogue_file}")
        return []
    except Exception as e:
        logger.error(f"Error loading catalogue: {e}")
        return []

def load_part_cost(part_id):
    try:
        parts_file = os.path.join(BASE_DIR, 'data', 'output.txt')
        with open(parts_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) >= 8 and parts[0] == part_id:
                        try:
                            return float(parts[7])
                        except ValueError:
                            logger.warning(f"Invalid cost format for {part_id}: {parts[7]}")
                            continue
        logger.debug(f"No cost found for part {part_id}")
        return None
    except FileNotFoundError:
        logger.error(f"Parts file not found: {parts_file}")
        return None
    except Exception as e:
        logger.error(f"Error loading part cost: {e}")
        return None

def handle_errors(description, input_data_func):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                self.show_message("Success", f"{description} completed: {result}", 'info')
                return result
            except Exception as e:
                output = f"{description} failed: {str(e)}"
                logger.error(f"{output}\nInput: {input_data_func(self)}")
                self.show_message("Error", output, 'error')
                raise
        return wrapper
    return decorator