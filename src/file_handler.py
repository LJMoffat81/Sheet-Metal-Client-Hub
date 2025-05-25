import os
import json
import logging
import hashlib

# Set up logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'data', 'log')
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'main_output.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class FileHandler:
    """Handle file operations and user authentication for Sheet Metal Client Hub."""

    def __init__(self):
        """Initialize data directory."""
        self.data_dir = os.path.join(BASE_DIR, 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        logging.debug(f"Initialized FileHandler with data directory: {self.data_dir}")

    def file_exists(self, filename):
        """Check if a file exists."""
        try:
            path = os.path.join(self.data_dir, filename)
            exists = os.path.exists(path)
            logging.debug(f"Checked file existence: {path}, exists: {exists}")
            return exists
        except Exception as e:
            logging.error(f"Error checking file existence {filename}: {e}")
            return False

    def read_file(self, filename):
        """Read content from a file."""
        try:
            with open(os.path.join(self.data_dir, filename), 'r') as f:
                content = f.read()
                logging.debug(f"Read file: {filename}")
                return content
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
            logging.debug(f"Wrote to file: {filename}")
        except Exception as e:
            logging.error(f"Error writing to file {filename}: {e}")

    def process_file(self, filename):
        """Process a file and return its lines as a list."""
        try:
            if not filename:
                logging.error("Empty filename provided")
                raise ValueError("Filename cannot be empty")
            content = self.read_file(filename)
            if content:
                lines = [line.strip() for line in content.splitlines() if line.strip()]
                logging.debug(f"Processed file {filename}, {len(lines)} lines")
                return lines
            return []
        except Exception as e:
            logging.error(f"Error processing file {filename}: {e}")
            return []

    def load_rates(self, filename):
        """Load rates from a JSON file."""
        try:
            path = os.path.join(self.data_dir, filename)
            with open(path, 'r') as f:
                rates = json.load(f)
                logging.debug(f"Loaded rates from: {path}")
                return rates
        except FileNotFoundError:
            logging.error(f"Rates file not found: {filename}")
            return {}
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in rates file: {filename}")
            return {}
        except Exception as e:
            logging.error(f"Error loading rates {filename}: {e}")
            return {}

    def save_output(self, part_id, revision, material, thickness, length, width, quantity, total_cost, fastener_types_and_counts, work_centres):
        """Save part output to a file."""
        try:
            path = os.path.join(self.data_dir, 'output.txt')
            output_line = f"{part_id},{revision},{material},{thickness},{length},{width},{quantity},{total_cost},{fastener_types_and_counts},{work_centres}\n"
            with open(path, 'a') as f:
                f.write(output_line)
            logging.debug(f"Saved output to: {path}")
        except Exception as e:
            logging.error(f"Error saving output: {e}")

    def save_quote(self, part_id, total_cost, customer_name, profit_margin, fastener_types_and_counts):
        """Save quote to a file."""
        try:
            path = os.path.join(self.data_dir, 'quotes.txt')
            quote_line = f"{part_id},{total_cost},{customer_name},{profit_margin},{fastener_types_and_counts}\n"
            with open(path, 'a') as f:
                f.write(quote_line)
            logging.debug(f"Saved quote to: {path}")
        except Exception as e:
            logging.error(f"Error saving quote: {e}")

    def update_rates(self, rate_key, rate_value):
        """Update a rate in the rates file."""
        try:
            path = os.path.join(self.data_dir, 'rates_global.txt')
            rates = self.load_rates('rates_global.txt')
            rates[rate_key] = rate_value
            with open(path, 'w') as f:
                json.dump(rates, f, indent=4)
            logging.debug(f"Updated rate {rate_key} to {rate_value} in: {path}")
        except Exception as e:
            logging.error(f"Error updating rates: {e}")

    def validate_credentials(self, username, password):
        """Validate user credentials using hashed passwords."""
        try:
            # Hardcoded users with SHA-256 hashed passwords
            users = {
                'laurie': '4b5a1911ddfde19a819157e85312b4aae8915e4968cb983e570da2e1098457e0',  # Hash of 'moffat123'
                'admin': '1b3231655cebb7a1f783eddf27d254ca7e6c8b89e4f69f7f63f0cfbdc9b5f6e4'   # Hash of 'admin123'
            }
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            logging.debug(f"Input hash for {username}: {hashed_password}")
            valid = username in users and users[username] == hashed_password
            logging.debug(f"Validated credentials for {username}: {'success' if valid else 'failure'}")
            return valid
        except Exception as e:
            logging.error(f"Error validating credentials: {e}")
            return False