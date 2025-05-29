import re
import logging
from calculator import calculate_cost
from logger import log_test_result
from logging_config import setup_logger

# Set up logging
logger = setup_logger('logic', 'logic.log')

def calculate_and_save(part_specs, file_handler, rates, added_parts, show_message):
    """
    Calculate cost and save output based on part specifications (FR2, FR3, FR4, FR5).
    Updates added_parts and returns the total cost.
    """
    logger.info("Calculating and saving part specifications")
    part_type = part_specs['part_type']
    part_id = part_specs['part_id']
    revision = part_specs['revision']
    specs = part_specs['specs']
    work_centres = part_specs['work_centres']

    if not all([part_id, revision]):
        logger.error("Part ID or Revision missing")
        raise ValueError("Part ID and Revision are required")

    if part_type == "Single Part":
        validations = [
            (specs['length'], 50, 3000, "Lay-Flat length must be between 50 and 3000 mm"),
            (specs['width'], 50, 1500, "Lay-Flat width must be between 50 and 1500 mm"),
            (specs['thickness'], 1.0, 3.0, "Thickness must be between 1.0 and 3.0 mm"),
            (specs['quantity'], 1, float('inf'), "Quantity must be a positive integer")
        ]
        normalized_material = specs['material'].lower()
        if normalized_material not in ['mild steel', 'aluminium', 'stainless steel']:
            logger.error(f"Invalid material: {normalized_material}")
            raise ValueError("Material must be 'Mild Steel', 'Aluminium', or 'Stainless Steel'")
        material_for_rates = {'mild steel': 'mild_steel_rate', 'aluminium': 'aluminium_rate', 'stainless steel': 'stainless_steel_rate'}[normalized_material]
    else:
        validations = [(specs['quantity'], 1, float('inf'), "Quantity must be a positive integer")]
        material_for_rates = "N/A"
        if not specs['sub_parts']:
            logger.error("No sub-parts selected for assembly")
            raise ValueError("At least one sub-part must be selected for an assembly")
        from utils import load_existing_parts
        existing_parts = load_existing_parts()
        for sub_part, _ in specs['sub_parts']:
            if sub_part not in existing_parts:
                logger.error(f"Sub-part {sub_part} not found")
                raise ValueError(f"Sub-part {sub_part} does not exist in the system")

    for value, min_val, max_val, error_msg in validations:
        if not (min_val <= value <= max_val):
            logger.error(f"Validation failed: {error_msg}")
            raise ValueError(error_msg)

    expected_prefix = "PART-" if part_type == "Single Part" else "ASSY-"
    if not part_id.startswith(expected_prefix) or not re.match(rf"^{expected_prefix}[A-Za-z0-9]{{5,15}}$", part_id):
        logger.error(f"Invalid part ID format: {part_id}")
        raise ValueError(f"Part ID must be {expected_prefix}[5-15 alphanumeric]")

    if not work_centres:
        logger.error("No WorkCentre operations selected")
        raise ValueError("At least one WorkCentre operation must be selected")

    if specs['sub_parts']:
        for item_id, _, count in specs['sub_parts']:
            if count > 100:
                logger.error(f"Fastener count too high for {item_id}: {count}")
                raise ValueError(f"Fastener count for {item_id} must be 0-100")

    catalogue_cost = 0.0
    if part_type == "Single Part":
        from utils import load_parts_catalogue
        catalogue = load_parts_catalogue()
        for item_id, _, count in specs['sub_parts']:
            for cat_id, _, price in catalogue:
                if item_id == cat_id:
                    catalogue_cost += price * count
                    logger.debug(f"Added catalogue cost: {price} x {count} for {item_id}")
                    break

    part_specs_full = {
        'part_type': part_type, 'part_id': part_id, 'revision': revision,
        'material': material_for_rates, 'thickness': specs['thickness'],
        'length': specs['length'], 'width': specs['width'], 'quantity': specs['quantity'],
        'sub_parts': specs['sub_parts'], 'top_level_assembly': specs['top_level_assembly'],
        'weldment_indicator': specs['weldment_indicator'], 'catalogue_cost': catalogue_cost,
        'work_centres': work_centres, 'fastener_types_and_counts': specs['fastener_types_and_counts']
    }

    if not rates:
        logger.error("Failed to load rates")
        raise ValueError("Failed to load rates from data/rates.json")

    total_cost = calculate_cost(part_specs_full, rates)
    if total_cost == 0.0:
        logger.error("Cost calculation returned zero")
        raise ValueError("Cost calculation failed, check inputs or rates")

    file_handler.save_output(
        part_id, revision, specs['material'], specs['thickness'],
        specs['length'], specs['width'], specs['quantity'], total_cost,
        specs['fastener_types_and_counts'], work_centres
    )
    added_parts.append({'part_id': part_id, 'quantity': specs['quantity']})
    logger.info(f"Part {part_id} saved with total cost £{total_cost}")
    log_test_result("Add Part to Parts List", f"Part ID: {part_id}, Quantity: {specs['quantity']}", f"Part {part_id} added", "Pass")
    show_message("Success", f"Cost calculated: £{total_cost}\nSaved to data/output.txt", 'info')
    return total_cost

def generate_quote(customer_name, profit_margin, added_parts, file_handler, show_message):
    """
    Generate and save a quote for all added parts (FR7).
    """
    logger.info("Generating quote for all added parts")
    try:
        profit_margin = float(profit_margin)
        logger.debug(f"Profit margin set to {profit_margin}%")
    except ValueError:
        logger.error("Invalid profit margin format")
        raise ValueError("Profit margin must be a valid number")
    if not customer_name:
        logger.error("Customer name empty")
        raise ValueError("Customer name cannot be empty")
    if profit_margin < 0:
        logger.error(f"Negative profit margin: {profit_margin}")
        raise ValueError("Profit margin cannot be negative")
    if not added_parts:
        logger.error("No parts added to quote")
        raise ValueError("No parts added to quote")

    from utils import load_part_cost
    part_details = []
    total_cost = 0.0
    for part in added_parts:
        part_id = part['part_id']
        quantity = part['quantity']
        unit_cost = load_part_cost(part_id)
        if unit_cost is None:
            logger.error(f"Cost not found for part {part_id}")
            raise ValueError(f"Cost not found for part {part_id}")
        part_total = unit_cost * quantity
        total_cost += part_total
        part_details.append({'part_id': part_id, 'quantity': quantity, 'unit_cost': unit_cost, 'total_cost': part_total})
        logger.debug(f"Added part {part_id}: quantity={quantity}, unit_cost=£{unit_cost}, total=£{part_total}")

    final_cost = total_cost * (1 + profit_margin / 100)
    fastener_types_and_counts = []
    file_handler.save_quote(part_details, final_cost, customer_name, profit_margin, fastener_types_and_counts)
    logger.info(f"Quote generated: total £{final_cost:.2f} for {len(part_details)} parts")
    show_message("Success", f"Quote generated for {len(part_details)} parts, total £{final_cost:.2f}, saved to data/quotes.txt", 'info')
    return final_cost

def update_rate(rate_key, rate_value, sub_value, file_handler, show_message):
    """
    Update a rate in rates.json (FR6).
    """
    logger.info("Updating rate")
    if rate_key == "Select Rate Key":
        logger.error("No rate key selected")
        raise ValueError("Please select a rate key")

    try:
        rate_value = float(rate_value)
        logger.debug(f"Rate value set to {rate_value}")
    except ValueError:
        logger.error("Invalid rate value format")
        raise ValueError("Rate value must be a valid number")

    if rate_value < 0:
        logger.error(f"Negative rate value: {rate_value}")
        raise ValueError("Rate value cannot be negative")

    rates = file_handler.load_rates()
    sub_value_float = None
    if rates[rate_key].get('type') == 'hourly' and rates[rate_key].get('sub_field'):
        try:
            sub_value_float = float(sub_value)
            logger.debug(f"Sub value set to {sub_value_float}")
        except ValueError:
            logger.error(f"Invalid sub value format for {rates[rate_key]['sub_field']}")
            raise ValueError(f"{rates[rate_key]['sub_field']} must be a valid number")
        if sub_value_float <= 0:
            logger.error(f"Non-positive sub value: {sub_value_float}")
            raise ValueError(f"{rates[rate_key]['sub_field']} must be positive")

    file_handler.update_rates(rate_key, rate_value, sub_value_float)
    logger.info(f"Rate '{rate_key}' updated to {rate_value}{f', {sub_value_float} {rates[rate_key]['sub_field']}' if sub_value_float else ''}")
    show_message("Success", f"Rate '{rate_key}' updated to {rate_value}{f', {sub_value_float} {rates[rate_key]['sub_field']}' if sub_value_float else ''}", 'info')
    return rate_value

def create_user(username, password, role, file_handler, show_message):
    """
    Create a new user with specified username, password, and role.
    """
    logger.info("Creating new user")
    if not username or not password:
        logger.error("Username or password empty")
        raise ValueError("Username and password cannot be empty")
    if not re.match(r"^[a-zA-Z0-9_]{3,20}$", username):
        logger.error(f"Invalid username format: {username}")
        raise ValueError("Username must be 3-20 alphanumeric characters or underscores")
    if len(password) < 6:
        logger.error("Password too short")
        raise ValueError("Password must be at least 6 characters")
    if role not in ["User", "Admin"]:
        logger.error(f"Invalid role: {role}")
        raise ValueError("Invalid role selected")

    from utils import hash_password
    hashed_password = hash_password(password)
    if hashed_password is None:
        logger.error("Failed to hash password")
        raise ValueError("Error processing password")

    file_handler.create_user(username, hashed_password, role)
    logger.info(f"User {username} created with role {role}")
    show_message("Success", f"User {username} created with role {role}", 'info')
    return username

def remove_user(username, file_handler, show_message):
    """
    Remove a user from users.json.
    """
    logger.info("Removing user")
    if username == "Select User":
        logger.error("No user selected for removal")
        raise ValueError("Please select a user to remove")

    file_handler.remove_user(username)
    logger.info(f"User {username} removed")
    show_message("Success", f"User {username} removed", 'info')
    return username