import os
import json
import logging

# Set up logging
logging.basicConfig(filename='file_handler.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Define BASE_DIR as the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class FileHandler:
    def process_file(self, filename):
        """Return the full path for a given filename."""
        return os.path.join(BASE_DIR, 'data', filename)

    def read_file(self, filename):
        """Read content from a file."""
        full_path = os.path.join(BASE_DIR, 'data', filename)
        logging.debug(f"Reading file: {full_path}")
        try:
            with open(full_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            logging.warning(f"File not found: {full_path}")
            return ""
        except Exception as e:
            logging.error(f"Error reading file {full_path}: {e}")
            raise

    def write_file(self, filename, content):
        """Write content to a file."""
        full_path = os.path.join(BASE_DIR, 'data', filename)
        logging.debug(f"Writing to file: {full_path}")
        try:
            with open(full_path, 'w') as f:
                f.write(content)
        except Exception as e:
            logging.error(f"Error writing to file {full_path}: {e}")
            raise

    def file_exists(self, filename):
        """Check if a file exists."""
        full_path = os.path.join(BASE_DIR, 'data', filename)
        logging.debug(f"Checking if file exists: {full_path}")
        return os.path.exists(full_path)

    def load_rates(self, rates_file):
        """Load rates from a JSON file."""
        full_path = os.path.join(BASE_DIR, 'data', rates_file)
        logging.debug(f"Loading rates from: {full_path}")
        if not os.path.exists(full_path) or os.path.getsize(full_path) == 0:
            logging.warning(f"Rates file {full_path} is empty or missing")
            return {}
        try:
            with open(full_path, 'r') as f:
                data = f.read().strip()
                if not data:
                    logging.warning(f"Rates file {full_path} is empty")
                    return {}
                return json.loads(data)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON in {full_path}: {e}")
            return {}
        except Exception as e:
            logging.error(f"Error loading rates from {full_path}: {e}")
            raise

    def validate_credentials(self, username, password):
        """Validate user credentials."""
        credentials_file = os.path.join(BASE_DIR, 'data', 'users.txt')
        logging.debug(f"Validating credentials against: {credentials_file}")
        if os.path.exists(credentials_file):
            try:
                with open(credentials_file, 'r') as f:
                    for line in f:
                        stored_user, stored_pass = line.strip().split(':')
                        if username == stored_user and password == stored_pass:
                            logging.info(f"Credentials validated for user: {username}")
                            return True
            except Exception as e:
                logging.error(f"Error validating credentials: {e}")
                return False
        logging.warning(f"Invalid credentials for user: {username}")
        return False

    def save_output(self, part_id, revision, material, thickness, length, width, quantity, total_cost):
        """Save output data to a file."""
        full_path = os.path.join(BASE_DIR, 'data', 'output.txt')
        logging.debug(f"Saving output to: {full_path}")
        try:
            with open(full_path, 'a') as f:
                f.write(f"{part_id},{revision},{material},{thickness},{length},{width},{quantity},{total_cost}\n")
        except Exception as e:
            logging.error(f"Error saving output to {full_path}: {e}")
            raise

    def save_quote(self, part_id, total_cost, customer_name, profit_margin):
        """Save quote data to a JSON file, one JSON object per line."""
        full_path = os.path.join(BASE_DIR, 'data', 'quotes.txt')
        quote_data = {
            'part_id': part_id,
            'total_cost': total_cost,
            'customer_name': customer_name,
            'profit_margin': profit_margin
        }
        logging.debug(f"Saving quote to: {full_path}")
        try:
            with open(full_path, 'a') as f:
                json.dump(quote_data, f)
                f.write('\n')
        except Exception as e:
            logging.error(f"Error saving quote to {full_path}: {e}")
            raise

    def update_rates(self, rate_key, rate_value):
        """Update rates in a JSON file."""
        rates_file = 'rates_global.txt'
        full_path = os.path.join(BASE_DIR, 'data', rates_file)
        logging.debug(f"Updating rates in: {full_path}")
        rates = self.load_rates(rates_file)
        rates[rate_key] = rate_value
        try:
            with open(full_path, 'w') as f:
                json.dump(rates, f, indent=4)
            logging.info(f"Updated rate {rate_key} to {rate_value}")
        except Exception as e:
            logging.error(f"Failed to update rates: {e}")
            raise
