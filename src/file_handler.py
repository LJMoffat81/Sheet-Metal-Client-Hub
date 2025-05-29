import json
import os
import logging
from logging_config import setup_logger

# Set up logging
logger = setup_logger('file_handler', 'file_handler.log')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class FileHandler:
    def __init__(self):
        self.users_file = os.path.join(BASE_DIR, 'data', 'users.json')
        self.rates_file = os.path.join(BASE_DIR, 'data', 'rates.json')
        self.output_file = os.path.join(BASE_DIR, 'data', 'output.txt')
        self.quotes_file = os.path.join(BASE_DIR, 'data', 'quotes.txt')
        logger.info("FileHandler initialized")

    def validate_credentials(self, username, hashed_password):
        """
        Validate user credentials against users.json.
        """
        logger.info(f"Validating credentials for username: {username}")
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            if username in users and users[username]['password'] == hashed_password:
                logger.info(f"Credentials validated for {username}")
                return True
            logger.debug(f"Validation failed for {username}")
            return False
        except FileNotFoundError:
            logger.error(f"Users file not found: {self.users_file}")
            return False
        except Exception as e:
            logger.error(f"Error validating credentials: {e}")
            return False

    def get_user_role(self, username):
        """
        Get the role of a user from users.json.
        """
        logger.info(f"Retrieving role for username: {username}")
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            role = users.get(username, {}).get('role')
            logger.debug(f"Role for {username}: {role}")
            return role
        except FileNotFoundError:
            logger.error(f"Users file not found: {self.users_file}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving role: {e}")
            return None

    def load_rates(self):
        """
        Load rates from rates.json.
        """
        logger.info("Loading rates")
        try:
            with open(self.rates_file, 'r', encoding='utf-8') as f:
                rates = json.load(f)
            logger.debug(f"Loaded {len(rates)} rates")
            return rates
        except FileNotFoundError:
            logger.error(f"Rates file not found: {self.rates_file}")
            return {}
        except Exception as e:
            logger.error(f"Error loading rates: {e}")
            return {}

    def save_output(self, part_id, revision, material, thickness, length, width, quantity, total_cost, fastener_types, work_centres):
        """
        Save part output to output.txt.
        """
        logger.info(f"Saving output for part {part_id}")
        try:
            with open(self.output_file, 'a', encoding='utf-8') as f:
                work_centres_str = ";".join([f"{wc[0]}:{wc[1]}:{wc[2]}" for wc in work_centres])
                f.write(f"{part_id},{revision},{material},{thickness},{length},{width},{quantity},{total_cost},{fastener_types},{work_centres_str}\n")
            logger.debug(f"Output saved for {part_id}")
        except Exception as e:
            logger.error(f"Error saving output: {e}")

    def save_quote(self, part_details, final_cost, customer_name, profit_margin, fastener_types):
        """
        Save quote to quotes.txt.
        """
        logger.info(f"Saving quote for customer {customer_name}")
        try:
            with open(self.quotes_file, 'a', encoding='utf-8') as f:
                parts_str = ";".join([f"{p['part_id']}:{p['quantity']}:{p['unit_cost']}" for p in part_details])
                f.write(f"{customer_name},{final_cost},{profit_margin},{parts_str},{fastener_types}\n")
            logger.debug(f"Quote saved for {customer_name}")
        except Exception as e:
            logger.error(f"Error saving quote: {e}")

    def create_user(self, username, hashed_password, role):
        """
        Create a new user in users.json.
        """
        logger.info(f"Creating user {username}")
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            if username in users:
                logger.error(f"User {username} already exists")
                raise ValueError("User already exists")
            users[username] = {'password': hashed_password, 'role': role}
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=4)
            logger.debug(f"User {username} created with role {role}")
        except FileNotFoundError:
            logger.error(f"Users file not found: {self.users_file}")
            users = {username: {'password': hashed_password, 'role': role}}
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=4)
            logger.debug(f"Created users file with user {username}")
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise

    def remove_user(self, username):
        """
        Remove a user from users.json.
        """
        logger.info(f"Removing user {username}")
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            if username not in users:
                logger.error(f"User {username} not found")
                raise ValueError("User not found")
            del users[username]
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=4)
            logger.debug(f"User {username} removed")
        except FileNotFoundError:
            logger.error(f"Users file not found: {self.users_file}")
            raise
        except Exception as e:
            logger.error(f"Error removing user: {e}")
            raise

    def get_all_usernames(self):
        """
        Get all usernames from users.json.
        """
        logger.info("Retrieving all usernames")
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            usernames = list(users.keys())
            logger.debug(f"Retrieved {len(usernames)} usernames")
            return usernames
        except FileNotFoundError:
            logger.error(f"Users file not found: {self.users_file}")
            return []
        except Exception as e:
            logger.error(f"Error retrieving usernames: {e}")
            return []

    def update_rates(self, rate_key, rate_value, sub_value):
        """
        Update a rate in rates.json.
        """
        logger.info(f"Updating rate {rate_key}")
        try:
            with open(self.rates_file, 'r', encoding='utf-8') as f:
                rates = json.load(f)
            if rate_key not in rates:
                logger.error(f"Rate key {rate_key} not found")
                raise ValueError("Rate key not found")
            rates[rate_key]['value'] = rate_value
            if sub_value is not None:
                rates[rate_key]['sub_value'] = sub_value
            with open(self.rates_file, 'w', encoding='utf-8') as f:
                json.dump(rates, f, indent=4)
            logger.debug(f"Rate {rate_key} updated to {rate_value}{f', sub_value={sub_value}' if sub_value else ''}")
        except FileNotFoundError:
            logger.error(f"Rates file not found: {self.rates_file}")
            raise
        except Exception as e:
            logger.error(f"Error updating rate: {e}")
            raise