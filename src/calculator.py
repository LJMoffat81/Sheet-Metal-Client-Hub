def calculate_cost(part_specs, rates):
    """
    Calculate total cost for a part or assembly based on specifications and rates.
    
    Args:
        part_specs (dict): Specifications including part_type, material, thickness, length, width,
                          quantity, sub_parts, catalogue_cost, work_centres, weldment_indicator.
        rates (dict): Rates loaded from data/rates_global.txt (e.g., mild_steel_rate, welding_rate_per_mm).
    
    Returns:
        float: Total cost in GBP, or 0.0 if calculation fails.
    """
    try:
        total_cost = 0.0

        # Normalize material name for rate key
        material_map = {
            'mild steel': 'mild_steel',
            'aluminium': 'aluminium',
            'stainless steel': 'stainless_steel'
        }

        # Material cost for single parts
        if part_specs['part_type'] == 'Single Part':
            material = part_specs['material'].lower()
            normalized_material = material_map.get(material, material)
            thickness = float(part_specs['thickness'])
            length = float(part_specs['length'])
            width = float(part_specs['width'])
            material_rate_key = f"{normalized_material}_rate"
            if material_rate_key in rates:
                # Calculate material cost: rate * thickness * area (length * width in mm²)
                material_cost = rates[material_rate_key] * thickness * length * width / 1000  # Convert to GBP
                total_cost += material_cost
            else:
                print(f"Error: Missing rate for {material_rate_key}")
                return 0.0

        # Catalogue cost (e.g., fasteners)
        catalogue_cost = float(part_specs.get('catalogue_cost', 0.0))
        total_cost += catalogue_cost

        # Work centre costs
        for work_centre, quantity in part_specs.get('work_centres', []):
            work_centre = work_centre.lower()
            rate_key = None
            if work_centre == 'cutting':
                rate_key = 'cutting_rate_per_mm'
            elif work_centre == 'bending':
                rate_key = 'bending_rate_per_bend'
            elif work_centre == 'welding':
                rate_key = 'welding_rate_per_mm'
            elif work_centre == 'assembly':
                rate_key = 'assembly_rate_per_component'
            elif work_centre == 'finishing':
                rate_key = 'finishing_rate_per_mm2'
            elif work_centre == 'drilling':
                rate_key = 'drilling_rate_per_hole'
            elif work_centre == 'punching':
                rate_key = 'punching_rate_per_punch'
            elif work_centre == 'grinding':
                rate_key = 'grinding_rate_per_mm2'
            elif work_centre == 'coating':
                rate_key = 'coating_rate_per_mm2'
            elif work_centre == 'inspection':
                rate_key = 'inspection_rate_per_inspection'

            if rate_key and rate_key in rates:
                # Apply default factor modifier (e.g., welding_factor_spot)
                factor_key = f"{work_centre}_factor_standard"  # Default factor
                factor = rates.get(factor_key, 1.0)  # Use 1.0 if factor missing
                cost = rates[rate_key] * float(quantity) * factor
                total_cost += cost
            else:
                print(f"Error: Missing rate for {rate_key}")
                return 0.0

        # Apply quantity multiplier for assemblies
        if part_specs['part_type'] == 'Assembly':
            quantity = int(part_specs['quantity'])
            total_cost *= quantity

        return round(total_cost, 2)
    except Exception as e:
        print(f"Error in calculate_cost: {e}")
        return 0.0
