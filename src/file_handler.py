import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def validate_credentials(username, password):
    """
    Validate user credentials against data/users.txt.
    """
    file_path = os.path.join(BASE_DIR, 'data/users.txt')
    try:
        with open(file_path, 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split(':')
                if username == stored_username and password == stored_password:
                    return True
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
    except Exception as e:
        print(f"Error validating credentials: {e}")
    return False

def load_rates():
    """
    Load rates from data/rates_global.txt.
    Expected format: key=value (e.g., cutting_rate_per_mm=0.05)
    Ignores lines starting with #, empty lines, or invalid formats.
    Returns: Dictionary of rates (key: rate name, value: float).
    """
    rates = {}
    file_path = os.path.join(BASE_DIR, 'data/rates_global.txt')
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines or comments
                if not line or line.startswith('#'):
                    continue
                # Skip lines that don't contain '='
                if '=' not in line:
                    continue
                try:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    rates[key] = float(value)
                except ValueError:
                    print(f"Warning: Skipping invalid line in {file_path}: {line}")
                    continue
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
    except Exception as e:
        print(f"Error loading rates: {e}")
    return rates

def save_output(part_id, revision, material, thickness, length, width, quantity, total_cost):
    """
    Save cost calculation output to data/output.txt.
    """
    file_path = os.path.join(BASE_DIR, 'data/output.txt')
    try:
        with open(file_path, 'a') as f:
            line = f"{part_id},{revision},{material},{thickness},{length},{width},{quantity},{total_cost}\n"
            f.write(line)
    except Exception as e:
        print(f"Error saving output: {e}")

def save_quote(part_id, total_cost, customer_name, profit_margin):
    """
    Save quote to data/quotes.txt.
    """
    file_path = os.path.join(BASE_DIR, 'data/quotes.txt')
    try:
        with open(file_path, 'a') as f:
            line = f"{part_id},{customer_name},{total_cost},{profit_margin}\n"
            f.write(line)
    except Exception as e:
        print(f"Error saving quote: {e}")

def update_rates(rate_key, rate_value):
    """
    Update or add a rate in data/rates_global.txt.
    """
    file_path = os.path.join(BASE_DIR, 'data/rates_global.txt')
    rates = load_rates()
    rates[rate_key] = rate_value
    try:
        with open(file_path, 'w') as f:
            for key, value in rates.items():
                f.write(f"{key}={value}\n")
    except Exception as e:
        print(f"Error updating rates: {e}")
