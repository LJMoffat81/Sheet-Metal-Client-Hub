# file_handler.py
# Purpose: Handles file operations for user credentials, rates, cost outputs, and quotes.
# Supports FR1 (Login), FR5 (Store Output), FR6 (Update Rates), FR7 (Generate Quote).
# Reads/writes data files (users.txt, rates_global.txt, output.txt, quotes.txt) in the data/ directory.
# Uses absolute paths to ensure files are found regardless of working directory.
# Ensures robust error handling for file operations to prevent crashes.

import os
from datetime import datetime

# Get the absolute path to the repository's data/ directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def validate_credentials(username, password):
    """
    Validate user credentials against users.txt (FR1: Login).
    
    Parameters:
        username (str): User's username (e.g., "laurie").
        password (str): User's password (e.g., "moffat123").
    
    Returns:
        bool: True if credentials match an entry in users.txt, False otherwise.
    
    Logic:
        1. Checks if users.txt exists in data/ directory; creates it with default credentials if not.
        2. Opens users.txt in read mode using absolute path.
        3. Reads each line, splitting by ':' to get stored username and password.
        4. Compares input username and password with stored values.
        5. Returns True if a match is found, False if no match.
        6. Handles FileNotFoundError, PermissionError, and other exceptions gracefully.
    """
    users_file = os.path.join(DATA_DIR, 'users.txt')
    try:
        if not os.path.exists(users_file):
            print(f"Warning: {users_file} not found, creating with default credentials")
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(users_file, 'w') as f:
                f.write("laurie:moffat123\nadmin:admin123\n")
        with open(users_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    user, pwd = line.strip().split(':')
                    if user == username and pwd == password:
                        return True
                except ValueError:
                    print(f"Error: Malformed line in users.txt: {line.strip()}")
                    continue
        return False
    except PermissionError:
        print(f"Error: Permission denied accessing {users_file}")
        return False
    except Exception as e:
        print(f"Error validating credentials: {e}")
        return False

def load_rates():
    """
    Load rates from rates_global.txt for cost calculations and updates (FR3, FR6).
    
    Returns:
        dict: Dictionary of rates (e.g., {'steel_rate': 5.0, 'labour_rate': 20.0}).
              Returns empty dict if file not found or error occurs.
    
    Logic:
        1. Checks if rates_global.txt exists; creates it with default rates if not.
        2. Opens rates_global.txt in read mode using absolute path.
        3. Reads each line, splitting by ':' to get key (e.g., 'steel_rate') and value (e.g., '5.0').
        4. Converts value to float and stores in dictionary.
        5. Handles errors (FileNotFoundError, ValueError) by returning empty dict.
    """
    rates_file = os.path.join(DATA_DIR, 'rates_global.txt')
    rates = {}
    try:
        if not os.path.exists(rates_file):
            print(f"Warning: {rates_file} not found, creating with default rates")
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(rates_file, 'w') as f:
                f.write("steel_rate:5.0\naluminum_rate:7.0\nlabour_rate:20.0\nlaser_cutting:25.0\nbending:15.0\nwelding:30.0\npainting:10.0\nassembly:12.0\ninspection:8.0\npackaging:5.0\nturret_press:20.0\n")
        with open(rates_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    key, value = line.strip().split(':')
                    rates[key] = float(value)
                except ValueError:
                    print(f"Error: Malformed line in rates_global.txt: {line.strip()}")
                    continue
        return rates
    except PermissionError:
        print(f"Error: Permission denied accessing {rates_file}")
        return {}
    except Exception as e:
        print(f"Error loading rates: {e}")
        return {}

def save_output(part_id, revision, material, thickness, length, width, quantity, total_cost):
    """
    Save cost calculation details to output.txt (FR5: Store Output).
    
    Parameters:
        part_id (str): Part identifier (e.g., "PART-12345").
        revision (str): Revision code (e.g., "Rev A1").
        material (str): Material type (e.g., "steel").
        thickness (float): Thickness in mm.
        length (float): Length in mm.
        width (float): Width in mm.
        quantity (int): Number of parts.
        total_cost (float): Calculated cost in GBP.
    
    Logic:
        1. Checks for duplicate part_id.
        2. Generates timestamp.
        3. Writes details to output.txt.
        4. Handles errors.
    """
    if check_duplicate_part_id(part_id):
        print(f"Error: Part ID {part_id} already exists in output.txt")
        return
    output_file = os.path.join(DATA_DIR, 'output.txt')
    timestamp = datetime.now().strftime('%Y-%m-%d')
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(output_file, 'a') as f:
            f.write(f"{part_id},{revision},{material},{thickness},{length},{width},{quantity},{total_cost},{timestamp}\n")
    except PermissionError:
        print(f"Error: Permission denied writing to {output_file}")
    except Exception as e:
        print(f"Error saving output: {e}")

def save_quote(part_id, total_cost, customer_name, profit_margin):
    """
    Generate and save a quote to quotes.txt (FR7: Generate Quote).
    
    Parameters:
        part_id (str): Part identifier (e.g., "PART-12345").
        total_cost (float): Base cost from calculate_cost.
        customer_name (str): Customer name (e.g., "John Smith").
        profit_margin (float): Profit margin percentage (e.g., 20.0).
    
    Logic:
        1. Validates inputs (non-empty customer_name, non-negative profit_margin).
        2. Generates a unique quote number (e.g., QUOTE-2025-timestamp).
        3. Calculates quote total: base cost * (1 + profit_margin/100).
        4. Generates current timestamp (YYYY-MM-DD).
        5. Ensures data/ directory exists.
        6. Opens quotes.txt in append mode using absolute path.
        7. Writes a comma-separated line with quote details.
        8. Handles errors by logging them to prevent crashes.
    """
    quotes_file = os.path.join(DATA_DIR, 'quotes.txt')
    try:
        if not customer_name.strip():
            print("Error: Customer name cannot be empty")
            return
        profit_margin = float(profit_margin)
        if profit_margin < 0:
            print("Error: Profit margin cannot be negative")
            return
        quote_number = f"QUOTE-{datetime.now().strftime('%Y')}-{int(datetime.now().timestamp())}"
        quote_total = total_cost * (1 + profit_margin / 100)
        timestamp = datetime.now().strftime('%Y-%m-%d')
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(quotes_file, 'a') as f:
            f.write(f"{quote_number},{customer_name},{quote_total},{profit_margin},{timestamp},{part_id}\n")
    except ValueError:
        print("Error: Invalid profit margin, must be numeric")
    except PermissionError:
        print(f"Error: Permission denied writing to {quotes_file}")
    except Exception as e:
        print(f"Error saving quote: {e}")

def update_rates(rate_key, rate_value):
    """
    Update a rate in rates_global.txt (FR6: Update Rates).
    
    Parameters:
        rate_key (str): Rate identifier (e.g., "steel_rate").
        rate_value (float): New rate value in GBP (e.g., 6.0).
    
    Logic:
        1. Validates inputs (non-empty rate_key, numeric non-negative rate_value).
        2. Loads current rates from rates_global.txt.
        3. Updates the specified rate key with the new value.
        4. Ensures data/ directory exists.
        5. Opens rates_global.txt in write mode using absolute path.
        6. Writes all rates back to the file.
        7. Handles errors by logging them to prevent crashes.
    """
    rates_file = os.path.join(DATA_DIR, 'rates_global.txt')
    try:
        if not rate_key.strip():
            print("Error: Rate key cannot be empty")
            return
        rate_value = float(rate_value)
        if rate_value < 0:
            print("Error: Rate value cannot be negative")
            return
        rates = load_rates()
        rates[rate_key] = rate_value
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(rates_file, 'w') as f:
            for key, value in rates.items():
                f.write(f"{key}:{value}\n")
    except ValueError:
        print("Error: Invalid rate value, must be numeric")
    except PermissionError:
        print(f"Error: Permission denied writing to {rates_file}")
    except Exception as e:
        print(f"Error updating rates: {e}")

def check_duplicate_part_id(part_id):
    """
    Check if a part ID already exists in output.txt using linear search (FR2, J5RE47).
    
    Parameters:
        part_id (str): Part identifier to check.
    
    Returns:
        bool: True if part_id exists, False otherwise.
    
    Logic:
        1. Opens output.txt and searches line by line.
        2. Returns True if part_id matches the first field.
        3. Handles errors gracefully.
    """
    output_file = os.path.join(DATA_DIR, 'output.txt')
    try:
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                for line in f:
                    if line.strip() and part_id == line.strip().split(',')[0]:
                        return True
        return False
    except Exception as e:
        print(f"Error checking duplicate part ID: {e}")
        return False
