import os

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
