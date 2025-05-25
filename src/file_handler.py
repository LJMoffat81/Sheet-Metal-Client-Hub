import os
import json

class FileHandler:
    def process_file(self, filename):
        """Return the full path for a given filename."""
        return os.path.join("base_dir", filename)

    def read_file(self, filename):
        """Read content from a file."""
        full_path = os.path.join("base_dir", filename)
        with open(full_path, 'r') as f:
            return f.read()

    def write_file(self, filename, content):
        """Write content to a file."""
        full_path = os.path.join("base_dir", filename)
        with open(full_path, 'w') as f:
            f.write(content)

    def file_exists(self, filename):
        """Check if a file exists."""
        full_path = os.path.join("base_dir", filename)
        return os.path.exists(full_path)

    def load_rates(self, rates_file):
        """Load rates from a JSON file."""
        full_path = os.path.join("base_dir", rates_file)
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                return json.load(f)
        return {}

    def validate_credentials(self, username, password):
        """Validate user credentials (placeholder)."""
        # Replace with actual validation logic
        credentials_file = os.path.join("base_dir", "credentials.txt")
        if os.path.exists(credentials_file):
            with open(credentials_file, 'r') as f:
                for line in f:
                    stored_user, stored_pass = line.strip().split(':')
                    if username == stored_user and password == stored_pass:
                        return True
        return False

    def save_output(self, output_file, data):
        """Save output data to a file."""
        full_path = os.path.join("base_dir", output_file)
        with open(full_path, 'w') as f:
            f.write(str(data))

    def save_quote(self, quote_file, quote_data):
        """Save quote data to a JSON file."""
        full_path = os.path.join("base_dir", quote_file)
        with open(full_path, 'w') as f:
            json.dump(quote_data, f, indent=4)

    def update_rates(self, rates_file, new_rates):
        """Update rates in a JSON file."""
        full_path = os.path.join("base_dir", rates_file)
        with open(full_path, 'w') as f:
            json.dump(new_rates, f, indent=4)
