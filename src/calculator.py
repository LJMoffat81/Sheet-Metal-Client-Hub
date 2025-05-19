# calculator.py
# Purpose: Implements cost calculation for sheet metal parts (FR3: Calculate Cost, FR4: Display Cost).
# This module calculates the total cost based on material, labour, and process rates from rates_global.txt.
# It supports steel and aluminum materials, with thickness in mm and costs in GBP.
# Used by gui.py to compute and display costs for user-entered part specifications.

def calculate_cost(part_id, revision, material, thickness, length, width, quantity, rates):
    """
    Calculate the total cost for a part based on specifications and rates (FR3-FR4).
    
    Parameters:
        part_id (str): Unique identifier for the part (e.g., "PART-12345").
        revision (str): Revision code for the part (e.g., "Rev A1").
        material (str): Material type ("steel" or "aluminum").
        thickness (float): Material thickness in mm (1-3 mm as per project specs).
        length (float): Part length in mm.
        width (float): Part width in mm.
        quantity (int): Number of parts.
        rates (dict): Dictionary of rates from rates_global.txt (e.g., {'steel_rate': 5.0, 'labour_rate': 20.0}).
    
    Returns:
        float: Total cost in GBP, rounded to 2 decimal places.
               Returns 0.0 if an error occurs (e.g., invalid inputs or missing rates).
    
    Logic:
        1. Retrieves material rate (e.g., steel_rate) and labour rate from rates dictionary.
        2. Extracts process rates (e.g., laser_cutting, bending) for the 10 work centres.
        3. Calculates volume (thickness * length * width in mm³).
        4. Computes material cost (volume * material_rate * quantity).
        5. Computes labour cost (volume * labour_rate * quantity).
        6. Computes process cost (sum of process rates * quantity).
        7. Returns total cost (material_cost + labour_cost + process_cost).
        8. Handles errors (e.g., missing rates, invalid inputs) by returning 0.0 and logging the error.
    """
    try:
        material_rate = rates.get(material.lower() + '_rate', 0.0)
        labour_rate = rates.get('labour_rate', 20.0)
        process_rates = {k: v for k, v in rates.items() if k not in ['steel_rate', 'aluminum_rate', 'labour_rate']}
        
        volume = thickness * length * width
        material_cost = volume * material_rate * quantity
        labour_cost = volume * labour_rate * quantity
        process_cost = sum(rate * quantity for rate in process_rates.values())
        
        total_cost = material_cost + labour_cost + process_cost
        return round(total_cost, 2)
    except Exception as e:
        print(f"Error calculating cost: {e}")
        return 0.0
