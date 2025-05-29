import logging
from logging_config import setup_logger

# Set up logging
logger = setup_logger('calculator', 'calculator.log')

def calculate_cost(part_specs, rates):
    """
    Calculate the total cost for a part based on specifications and rates.
    """
    logger.info(f"Calculating cost for part {part_specs['part_id']}")
    try:
        total_cost = 0.0
        part_type = part_specs['part_type']
        quantity = part_specs['quantity']
        catalogue_cost = part_specs.get('catalogue_cost', 0.0)

        if part_type == "Single Part":
            material_rate = rates.get(part_specs['material'], {}).get('value', 0.0)
            area = part_specs['length'] * part_specs['width'] / 1_000_000  # m²
            material_cost = material_rate * area * part_specs['thickness'] * quantity
            total_cost += material_cost
            logger.debug(f"Material cost: £{material_cost} (area={area}m², thickness={part_specs['thickness']}mm)")

        for wc, qty, sub_option in part_specs['work_centres']:
            rate_key = f"{wc.lower()}_rate"
            rate = rates.get(rate_key, {}).get('value', 0.0)
            if rates.get(rate_key, {}).get('type') == 'hourly':
                sub_field = rates[rate_key].get('sub_field')
                sub_value = rates[rate_key].get('sub_value', 1.0)
                if sub_field and sub_value:
                    operation_cost = rate * (qty / sub_value) * quantity
                else:
                    operation_cost = rate * qty * quantity
            else:
                operation_cost = rate * qty * quantity
            total_cost += operation_cost
            logger.debug(f"Operation cost for {wc} ({sub_option}): £{operation_cost} (qty={qty})")

        total_cost += catalogue_cost * quantity
        logger.debug(f"Catalogue cost: £{catalogue_cost} x {quantity}")
        logger.info(f"Total cost for {part_specs['part_id']}: £{total_cost}")
        return total_cost
    except Exception as e:
        logger.error(f"Error calculating cost for {part_specs['part_id']}: {e}")
        return 0.0