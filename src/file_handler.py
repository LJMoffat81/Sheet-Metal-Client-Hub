# file_handler.py
# Purpose: Handles file operations for user credentials, rates, cost outputs, and quotes.
# Supports FR1 (Login), FR5 (Store Output), FR6 (Update Rates), FR7 (Generate Quote).
# Reads/writes data files (users.txt, rates_global.txt, output.txt, quotes.txt) in the data/ directory.
# Ensures robust error handling for file operations to prevent crashes.

import os
from datetime import datetime

def validate_credentials(username, password):
    """
    Validate user credentials against users.txt (FR1: Login).

    Parameters:
        username (str): User's username (e.g., "laurie").
        password (str): User's password (e.g., "moffat123").

    Returns:
        bool: True if credentials match an entry in users.txt, False otherwise.

    Logic:
        1. Opens users.txt in read mode.
        2. Reads each line, splitting by ':' to get stored username and password.
        3. Compares input username and password with stored values.
        4. Returns True if a match is found, False if no match.
        5. Handles FileNotFoundError by returning False and logging the error.
    """
    try:
        with open('data/users.txt', 'r') as f:
            for line in f:
                user, pwd = line.strip().split(':')
                if user == username and pwd == password:
                    return True
        return False
    except FileNotFoundError:
        print("users.txt not found")
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
        1. Opens rates_global.txt in read mode.
        2. Reads each line, splitting by ':' to get key (e.g., 'steel_rate') and value (e.g., '5.0').
        3. Converts value to float and stores in dictionary.
        4. Returns the rates dictionary.
        5. Handles FileNotFoundError by returning an empty dict and logging the error.
    """
    rates = {}
    try:
        with open('data/rates_global.txt', 'r') as f:
            for line in f:
                key, value = line.strip().split(':')
                rates[key] = float(value)
        return rates
    except FileNotFoundError:
        print("rates_global.txt not found")
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
        1. Generates current timestamp (YYYY-MM-DD).
        2. Opens output.txt in append mode.
        3. Writes a comma-separated line with part details, cost, and timestamp.
        4. Handles errors by logging them to prevent crashes.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d')
    try:
        with open('data/output.txt', 'a') as f:
            f.write(f"{part_id},{revision},{material},{thickness},{length},{width},{quantity},{total_cost},{timestamp}\n")
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
        1. Generates a unique quote number (e.g., QUOTE-2025-timestamp).
        2. Calculates quote total: base cost * (1 + profit_margin/100).
        3. Generates current timestamp (YYYY-MM-DD).
        4. Opens quotes.txt in append mode.
        5. Writes a comma-separated line with quote details.
        6. Handles errors by logging them to prevent crashes.
    """
    quote_number = f"QUOTE-{datetime.now().strftime('%Y')}-{int(datetime.now().timestamp())}"
    quote_total = total_cost * (1 + profit_margin / 100)
    timestamp = datetime.now().strftime('%Y-%m-%d')
    try:
        with open('data/quotes.txt', 'a') as f:
            f.write(f"{quote_number},{customer_name},{quote_total},{profit_margin},{timestamp},{part_id}\n")
    except Exception as e:
        print(f"Error saving quote: {e}")

def update_rates(rate_key, rate_value):
    """
    Update a rate in rates_global.txt (FR6: Update Rates).

    Parameters:
        rate_key (str): Rate identifier (e.g., "steel_rate").
        rate_value (float): New rate value in GBP (e.g., 6.0).

    Logic:
        1. Loads current rates from rates_global.txt.
        2. Updates the specified rate key with the new value.
        3. Opens rates_global.txt in write mode.
        4. Writes all rates back to the file.
        5. Handles errors by logging them to prevent crashes.
    """
    rates = load_rates()
    rates[rate_key] = float(rate_value)
    try:
        with open('data/rates_global.txt', 'w') as f:
            for key, value in rates.items():
                f.write(f"{key}:{value}\n")
    except Exception as e:
        print(f"Error updating rates: {e}")
