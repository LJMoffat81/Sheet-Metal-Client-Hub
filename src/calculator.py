import logging

# Set up logging
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'log')
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'main_output.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def calculate_cost(part_data, rates):
    """
    Calculate the total cost for a part or assembly based on specifications and rates.

    Args:
        part_data (dict): Specifications including part type, material, dimensions, etc.
        rates (dict): Rates for materials, operations, and fasteners.

    Returns:
        float: Total cost, or 0.0 if calculation fails.
    """
    try:
        logging.debug(f"Calculating cost for part_data: {part_data}")
        total_cost = 0.0
        part_type = part_data.get('part_type')
        material = part_data.get('material')
        thickness = float(part_data.get('thickness', 0))
        length = float(part_data.get('length', 0))
        width = float(part_data.get('width', 0))
        quantity = int(part_data.get('quantity', 1))
        work_centres = part_data.get('work_centres', [])
        catalogue_cost = float(part_data.get('catalogue_cost', 0.0))
        fastener_types_and_counts = part_data.get('fastener_types_and_counts', [])

        # Material cost for single parts
        if part_type == 'Single Part' and material != 'N/A':
            material_rate_key = material.lower()
            if material_rate_key not in rates:
                logging.error(f"Missing rate for {material_rate_key}")
                return 0.0
            material_cost = rates[material_rate_key] * thickness * length * width * quantity
            total_cost += material_cost
            logging.debug(f"Material cost: £{material_cost}")

        # WorkCentre costs
        for work_centre, qty, sub_option in work_centres:
            rate_key = None
            if work_centre == 'Cutting':
                rate_key = 'cutting_rate_per_mm'
            elif work_centre == 'Bending':
                rate_key = 'bending_rate_per_bend'
            elif work_centre == 'Welding':
                rate_key = 'mig_welding_rate_per_mm' if sub_option == 'MIG' else 'tig_welding_rate_per_mm'
            elif work_centre == 'Assembly':
                rate_key = 'assembly_rate_per_component'
            elif work_centre == 'Finishing':
                rate_key = 'finishing_rate_per_mm²'
            elif work_centre == 'Drilling':
                rate_key = 'drilling_rate_per_hole'
            elif work_centre == 'Punching':
                rate_key = 'punching_rate_per_punch'
            elif work_centre == 'Grinding':
                rate_key = 'grinding_rate_per_mm²'
            elif work_centre == 'Coating':
                rate_key = 'painting_rate_per_mm²' if sub_option == 'Painting' else 'coating_rate_per_mm²'
            elif work_centre == 'Inspection':
                rate_key = 'inspection_rate_per_unit'

            if rate_key and rate_key in rates:
                work_centre_cost = rates[rate_key] * qty * quantity
                total_cost += work_centre_cost
                logging.debug(f"{work_centre} cost: £{work_centre_cost}")
            else:
                logging.error(f"Missing rate for {rate_key or work_centre.lower() + '_rate'}")
                return 0.0

        # Fastener costs
        for fastener_type, count in fastener_types_and_counts:
            rate_key = f"{fastener_type.lower()}_rate_per_unit"
            if rate_key in rates:
                fastener_cost = rates[rate_key] * count * quantity
                total_cost += fastener_cost
                logging.debug(f"Fastener {fastener_type} cost: £{fastener_cost}")
            else:
                logging.error(f"Missing rate for {rate_key}")
                return 0.0

        # Catalogue cost
        total_cost += catalogue_cost * quantity
        logging.debug(f"Catalogue cost: £{catalogue_cost * quantity}")

        logging.info(f"Total cost calculated: £{total_cost}")
        return total_cost
    except Exception as e:
        logging.error(f"Error in cost calculation: {e}")
        return 0.0