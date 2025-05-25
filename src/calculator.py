import logging

logging.basicConfig(
    filename='calculator.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def calculate_cost(part_data, rates):
    """Calculate the cost of a part or assembly."""
    try:
        part_type = part_data.get('part_type', 'Single Part')
        quantity = part_data.get('quantity', 1)
        material = part_data.get('material', '')
        thickness = float(part_data.get('thickness', 0.0))
        length = float(part_data.get('length', 0.0))
        width = float(part_data.get('width', 0.0))
        work_centres = part_data.get('work_centres', [])
        catalogue_cost = part_data.get('catalogue_cost', 0.0)
        cost = 0.0

        if part_type == 'Assembly':
            components = part_data.get('quantity', 0)
            cost += rates.get('assembly_rate_per_component', 0) * components * quantity
        else:
            material_rate_key = f"{material.lower()}_rate"
            material_rate = rates.get(material_rate_key)
            if not material_rate:
                logging.error(f"Missing rate for {material_rate_key}")
                return 0.0

            area = length * width
            cost += material_rate * thickness * area * quantity

        for centre, qty in work_centres:
            if centre == 'Assembly' and part_type == 'Assembly':
                continue  # Skip assembly cost if already calculated
            rate_key = f"{centre.lower()}_rate_per_mm" if centre in ['Cutting', 'Welding', 'Finishing', 'Grinding', 'Coating'] else \
                       f"{centre.lower()}_rate_per_bend" if centre == 'Bending' else \
                       f"{centre.lower()}_rate_per_hole" if centre == 'Drilling' else \
                       f"{centre.lower()}_rate_per_punch" if centre == 'Punching' else \
                       f"{centre.lower()}_rate_per_inspection" if centre == 'Inspection' else \
                       f"{centre.lower()}_rate_per_component"
            rate = rates.get(rate_key)
            if not rate:
                logging.error(f"Missing rate for {rate_key}")
                return 0.0
            if centre == 'Cutting':
                perimeter = 2 * (length + width)
                cost += rate * qty * quantity
            elif centre in ['Welding', 'Finishing', 'Grinding', 'Coating']:
                cost += rate * qty * quantity
            elif centre in ['Bending', 'Drilling', 'Punching', 'Inspection']:
                cost += rate * qty * quantity
            elif centre == 'Assembly':
                cost += rate * qty * quantity

        cost += catalogue_cost * quantity

        logging.debug(f"Calculated cost: {cost} for part_data: {part_data}")
        return cost
    except Exception as e:
        logging.error(f"Error in calculate_cost: {str(e)}")
        return 0.0
