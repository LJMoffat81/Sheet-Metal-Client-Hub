import os
import json
import logging

class FileHandler:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, 'data')
        os.makedirs(self.data_dir, exist_ok=True)

    def file_exists(self, filename):
        """Check if a file exists."""
        try:
            return os.path.exists(os.path.join(self.data_dir, filename))
        except Exception as e:
            logging.error(f"Error checking file existence: {e}")
            return False

    def read_file(self, filename):
        """Read content from a file."""
        try:
            with open(os.path.join(self.data_dir, filename), 'r') as f:
                return f.read()
        except FileNotFoundError:
            logging.error(f"File not found: {filename}")
            return ""
        except Exception as e:
            logging.error(f"Error reading file {filename}: {e}")
            return ""

    def write_file(self, filename, content):
        """Write content to a file."""
        try:
            with open(os.path.join(self.data_dir, filename), 'w') as f:
                f.write(content)
        except Exception as e:
            logging.error(f"Error writing to file {filename}: {e}")

    def process_file(self, filename):
        """Process a file and return its lines as a list."""
        if not filename:
            logging.error("Empty filename provided")
            raise ValueError("Filename cannot be empty")
        content = self.read_file(filename)
        if content:
            return [line.strip() for line in content.splitlines() if line.strip()]
        return []

    def load_rates(self, filename):
        """Load rates from a JSON file."""
        try:
            with open(os.path.join(self.data_dir, filename), 'r') as f:
                logging.debug(f"Loading rates from: {os.path.join(self.data_dir, filename)}")
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Rates file not found: {filename}")
            return {}
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in rates file: {filename}")
            return {}
        except Exception as e:
            logging.error(f"Error loading rates: {e}")
            return {}

    def save_output(self, part_id, revision, material, thickness, length, width, quantity, total_cost, fastener_types_and_counts, work_centres):
        """Save part output to a file."""
        try:
            output_file = os.path.join(self.data_dir, 'output.txt')
            logging.debug(f"Saving output to: {output_file}")
            output_line = f"{part_id},{revision},{material},{thickness},{length},{width},{quantity},{total_cost},{fastener_types_and_counts},{work_centres}\n"
            with open(output_file, 'a') as f:
                f.write(output_line)
        except Exception as e:
            logging.error(f"Error saving output: {e}")

    def save_quote(self, part_id, total_cost, customer_name, profit_margin, fastener_types_and_counts):
        """Save quote to a file."""
        try:
            quotes_file = os.path.join(self.data_dir, 'quotes.txt')
            quote_line = f"{part_id},{total_cost},{customer_name},{profit_margin},{fastener_types_and_counts}\n"
            with open(quotes_file, 'a') as f:
                f.write(quote_line)
        except Exception as e:
            logging.error(f"Error saving quote: {e}")

    def update_rates(self, rate_key, rate_value):
        """Update a rate in the rates file."""
        try:
            rates_file = os.path.join(self.data_dir, 'rates_global.txt')
            rates = self.load_rates('rates_global.txt')
            rates[rate_key] = rate_value
            with open(rates_file, 'w') as f:
                json.dump(rates, f, indent=4)
        except Exception as e:
            logging.error(f"Error updating rates: {e}")

    def validate_credentials(self, username, password):
        """Validate user credentials."""
        # Simple hardcoded user store for testing
        users = {
            'laurin': 'moffat123',
            'admin': 'admin123'
        }
        try:
            return username in users and users[username] == password
        except Exception as e:
            logging.error(f"Error validating credentials: {e}")
            return False