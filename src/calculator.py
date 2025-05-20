# calculator.py
# Purpose: Implements cost calculation for sheet metal parts (FR3: Calculate Cost, FR4: Display Cost).
# Calculates total cost based on material, labour, and process rates, including work centre inputs.
# Supports assemblies and single parts, with costs in GBP and dimensions in mm.
# Used by gui.py to compute and display costs.

def calculate_cost(part_specs, rates):
    """
    Calculate the total cost for a part or assembly based on specifications and rates (FR3-FR4).
    
    Parameters:
        part_specs (dict): Dictionary with part specifications (e.g., part_type, material, cutting_method).
        rates (dict): Dictionary of rates from rates_global.txt (e.g., {'steel_rate': 5.0}).
    
    Returns:
        float: Total cost in GBP, rounded to 2 decimal places.
               Returns 0.0 if an error occurs.
    
    Logic:
        1. For assemblies, recursively calculate sub-part costs and add assembly costs.
        2. For single parts, compute material, labour, and work centre costs (e.g., cutting).
        3. Handles errors by returning 0.0 and logging.
    """
    try:
        total_cost = 0.0
        if part_specs['part_type'] == 'Assembly':
            for sub_part in part_specs.get('sub_parts', []):
                # Placeholder: Sub-parts need full specs in future
                sub_specs = {
                    'part_type': 'Single Part',
                    'material': part_specs['material'],
                    'thickness': part_specs['thickness'],
                    'length': part_specs['length'],
                    'width': part_specs['width'],
                    'quantity': 1,
                    'cutting_method': 'None',
                    'cutting_complexity': 0
                }
                total_cost += calculate_cost(sub_specs, rates)
            total_cost += rates.get('assembly', 0.0) * part_specs.get('assembly_components', 0)
        else:
            volume = part_specs['thickness'] * part_specs['length'] * part_specs['width']
            material_cost = volume * rates.get(f"{part_specs['material']}_rate", 0.0)
            labour_cost = volume * rates.get('labour_rate', 0.0)
            cutting_cost = (rates.get('laser_cutting', 0.0) * part_specs.get('cutting_complexity', 0)
                            if part_specs.get('cutting_method') == 'Laser Cutting' else
                            rates.get('turret_press', 0.0) * part_specs.get('cutting_complexity', 0)
                            if part_specs.get('cutting_method') == 'Turret Press Punching' else 0)
            total_cost = material_cost + labour_cost + cutting_cost  # Add other work centres later
        return round(total_cost * part_specs['quantity'], 2)
    except Exception as e:
        print(f"Error calculating cost: {e}")
        return 0.0
