import json
import logging
import os

# Set up logging
logging.basicConfig(
    filename='file_handler.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class FileHandler:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self):
        pass

    def read_file(self, filename):
        """Read content from a file."""
        filepath = os.path.join(self.BASE_DIR, filename)
        logging.debug(f"Reading file: {filepath}")
        try:
            with open(filepath, 'r') as file:
                return file.read()
        except FileNotFoundError:
            logging.error(f"File not found: {filepath}")
            return ""
        except Exception as e:
            logging.error(f"Error reading file {filepath}: {str(e)}")
            return ""

    def write_file(self, filename, content):
        """Write content to a file in append mode."""
        filepath = os.path.join(self.BASE_DIR, filename)
        logging.debug(f"Writing to file: {filepath}")
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'a') as file:
                file.write(content + '\n')
        except Exception as e:
            logging.error(f"Error writing to file {filepath}: {str(e)}")

    def file_exists(self, filename):
        """Check if a file exists."""
        filepath = os.path.join(self.BASE_DIR, filename)
        logging.debug(f"Checking if file exists: {filepath}")
        return os.path.exists(filepath)

    def process_file(self, filename):
        """Process file content."""
        content = self.read_file(filename)
        logging.debug(f"Processing file: {filename}")
        return content.upper() if content else ""

    def load_rates(self, filename='data/rates_global.txt'):
        """Load rates from rates_global.txt."""
        filepath = os.path.join(self.BASE_DIR, filename)
        logging.debug(f"Loading rates from: {filepath}")
        try:
            with open(filepath, 'r') as file:
                content = file.read().strip()
                if not content:
                    logging.warning(f"Rates file {filepath} is empty or missing")
                    return {}
                return json.loads(content)
        except FileNotFoundError:
            logging.warning(f"Rates file not found: {filepath}")
            return {}
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from {filepath}: {str(e)}")
            return {}
        except Exception as e:
            logging.error(f"Error loading rates from {filepath}: {str(e)}")
            return {}

    def save_output(self, part_id, revision, material, thickness, length, width, quantity, total_cost):
        """Save output data to output.txt, avoiding duplicates."""
        filepath = os.path.join(self.BASE_DIR, 'data', 'output.txt')
        logging.debug(f"Saving output to: {filepath}")
        output_data = f"{part_id},{revision},{material},{thickness},{length},{width},{quantity},{total_cost}"
        try:
            existing = set()
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    existing = {line.strip() for line in f if line.strip()}
            if output_data not in existing:
                with open(filepath, 'a') as file:
                    file.write(output_data + '\n')
        except Exception as e:
            logging.error(f"Error saving output to {filepath}: {str(e)}")

    def save_quote(self, part_id, total_cost, customer_name, profit_margin):
        """Save quote data to quotes.txt, avoiding duplicates."""
        filepath = os.path.join(self.BASE_DIR, 'data', 'quotes.txt')
        logging.debug(f"Saving quote to: {filepath}")
        quote_data = json.dumps({
            'part_id': part_id,
            'total_cost': total_cost * (1 + profit_margin / 100),
            'customer_name': customer_name,
            'profit_margin': profit_margin
        })
        try:
            existing = set()
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    for line in f:
                        if line.strip():
                            try:
                                quote = json.loads(line.strip())
                                key = (quote['part_id'], quote['customer_name'], quote['total_cost'])
                                existing.add(str(key))
                            except json.JSONDecodeError:
                                continue
            quote = json.loads(quote_data)
            key = (quote['part_id'], quote['customer_name'], quote['total_cost'])
            if str(key) not in existing:
                with open(filepath, 'a') as file:
                    file.write(quote_data + '\n')
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding quote JSON: {str(e)}")
        except Exception as e:
            logging.error(f"Error saving quote to {filepath}: {str(e)}")

    def validate_credentials(self, username, password):
        """Validate user credentials against users.txt."""
        filepath = os.path.join(self.BASE_DIR, 'data', 'users.txt')
        logging.debug(f"Validating credentials against: {filepath}")
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    if line.strip():
                        stored_username, stored_password = line.strip().split(':')
                        if username == stored_username and password == stored_password:
                            logging.info(f"Credentials validated for user: {username}")
                            return True
            logging.warning(f"Invalid credentials for user: {username}")
            return False
        except FileNotFoundError:
            logging.error(f"Users file not found: {filepath}")
            return False
        except Exception as e:
            logging.error(f"Error validating credentials: {str(e)}")
            return False

    def update_rates(self, key, value):
        """Update a rate in rates_global.txt."""
        filepath = os.path.join(self.BASE_DIR, 'data', 'rates_global.txt')
        logging.debug(f"Updating rates in: {filepath}")
        try:
            rates = self.load_rates()
            rates[key] = float(value)
            with open(filepath, 'w') as file:
                json.dump(rates, file, indent=4)
            logging.info(f"Updated rate {key} to {value}")
        except Exception as e:
            logging.error(f"Error updating rates in {filepath}: {str(e)}")
