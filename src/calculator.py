import logging

def calculate_cost(part_data, rates):
    """
    Calculate the total cost for a part or assembly based on specifications.
    """
    total_cost = 0.0
    try:
        part_type = part_data['part_type']
        material = part_data['material']
        thickness = float(part_data['thickness'])
        length = float(part_data['length'])
        width = float(part_data['width'])
        quantity = int(part_data['quantity'])
        work_centres = part_data['work_centres']
        catalogue_cost = float(part_data['catalogue_cost'])
        fastener_types_and_counts = part_data['fastener_types_and_counts']

        # Material cost for single parts
        if part_type == 'Single Part':
            if material in rates:
                material_rate = rates[material]
                total_cost += material_rate * thickness * length * width * quantity
            else:
                logging.error(f"Missing rate for {material}")
                return 0.0

        # Work centre costs
        for work_centre, qty, sub_option in work_centres:
            qty = float(qty)
            rate_key = None
            if work_centre == 'Cutting':
                rate_key = 'cutting_rate_per_mm'
            elif work_centre == 'Bending':
                rate_key = 'bending_rate_per_bend'
            elif work_centre == 'Welding':
                rate_key = 'mig_welding_rate_per_mm' if sub_option == 'MIG' else 'tig_welding_rate_per_mm'
            elif work_centre == 'Coating':
                rate_key = 'painting_rate_per_mm²' if sub_option == 'Painting' else 'coating_rate_per_mm²'
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
            elif work_centre == 'Inspection':
                rate_key = 'inspection_rate_per_unit'

            if rate_key and rate_key in rates:
                total_cost += rates[rate_key] * qty * quantity
            else:
                logging.error(f"Missing rate for {rate_key or work_centre}")
                return 0.0

        # Fastener costs
        for fastener_type, count in fastener_types_and_counts:
            rate_key = f"{fastener_type.lower()}_rate_per_unit"
            if rate_key in rates:
                total_cost += rates[rate_key] * count * quantity
            else:
                logging.error(f"Missing rate for {rate_key}")
                return 0.0

        # Catalogue cost
        total_cost += catalogue_cost * quantity

        return total_cost
    except (KeyError, ValueError) as e:
        logging.error(f"Error calculating cost: {e}")
        return 0.0