import os
import json

# Define BASE_DIR as the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class FileHandler:
    def process_file(self, filename):
        """Return the full path for a given filename."""
        return os.path.join(BASE_DIR, 'data', filename)

    def read_file(self, filename):
        """Read content from a file."""
        full_path = os.path.join(BASE_DIR, 'data', filename)
        with open(full_path, 'r') as f:
            return f.read()

    def write_file(self, filename, content):
        """Write content to a file."""
        full_path = os.path.join(BASE_DIR, 'data', filename)
        with open(full_path, 'w') as f:
            f.write(content)

    def file_exists(self, filename):
        """Check if a file exists."""
        full_path = os.path.join(BASE_DIR, 'data', filename)
        return os.path.exists(full_path)

    def load_rates(self, rates_file):
        """Load rates from a JSON file."""
        full_path = os.path.join(BASE_DIR, 'data', rates_file)
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                return json.load(f)
        return {}

    def validate_credentials(self, username, password):
        """Validate user credentials."""
        credentials_file = os.path.join(BASE_DIR, 'data', 'users.txt')
        if os.path.exists(credentials_file):
            with open(credentials_file, 'r') as f:
                for line in f:
                    stored_user, stored_pass = line.strip().split(':')
                    if username == stored_user and password == stored_pass:
                        return True
        return False

    def save_output(self, part_id, revision, material, thickness, length, width, quantity, total_cost):
        """Save output data to a file."""
        full_path = os.path.join(BASE_DIR, 'data', 'output.txt')
        with open(full_path, 'a') as f:
            f.write(f"{part_id},{revision},{material},{thickness},{length},{width},{quantity},{total_cost}\n")

    def save_quote(self, part_id, total_cost, customer_name, profit_margin):
        """Save quote data to a JSON file, one JSON object per line."""
        full_path = os.path.join(BASE_DIR, 'data', 'quotes.txt')
        quote_data = {
            'part_id': part_id,
            'total_cost': total_cost,
            'customer_name': customer_name,
            'profit_margin': profit_margin
        }
        with open(full_path, 'a') as f:
            json.dump(quote_data, f)
            f.write('\n')

    def update_rates(self, rate_key, rate_value):
        """Update rates in a JSON file."""
        rates_file = 'rates_global.txt'
        full_path = os.path.join(BASE_DIR, 'data', rates_file)
        rates = self.load_rates(rates_file)
        rates[rate_key] = rate_value
        with open(full_path, 'w') as f:
            json.dump(rates, f, indent=4)
