import logging

logging.basicConfig(
    filename='calculator.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def calculate_cost(part_data, rates):
    """Calculate the cost of a part or assembly."""
    try:
        part_type = part_data.get('part_type', 'Part')
        quantity = part_data.get('quantity', 1)
        cost = 0.0

        if part_type == 'Assembly':
            components = part_data.get('components', 0)
            cost += rates.get('assembly_rate_per_component', 0) * components * quantity
        else:
            material = part_data.get('material', '')
            thickness = part_data.get('thickness', 0.0)
            length = part_data.get('length', 0.0)
            width = part_data.get('width', 0.0)
            work_centres = part_data.get('work_centres', [])

            material_rate_key = f"{material.lower()}_rate"
            material_rate = rates.get(material_rate_key)
            if not material_rate:
                logging.error(f"Missing rate for {material_rate_key}")
                return 0.0

            area = length * width
            cost += material_rate * thickness * area * quantity

            for centre in work_centres:
                rate_key = f"{centre.lower()}_rate_per_mm" if centre in ['cutting', 'welding'] else f"{centre.lower()}_rate_per_bend"
                rate = rates.get(rate_key)
                if not rate:
                    logging.error(f"Missing rate for {rate_key}")
                    return 0.0
                if centre == 'cutting':
                    perimeter = 2 * (length + width)
                    cost += rate * perimeter * quantity
                elif centre == 'bending':
                    cost += rate * quantity
                elif centre == 'welding':
                    cost += rate * length * quantity

        logging.debug(f"Calculated cost: {cost} for part_data: {part_data}")
        return cost
    except Exception as e:
        logging.error(f"Error in calculate_cost: {str(e)}")
        return 0.0
