"""
Cost Estimation Logic
Calculates repair costs based on car category, damage type, and severity
"""

import sqlite3

# Car category multipliers
CAR_CATEGORY_MULTIPLIERS = {
    'economy': 1.0,      # Base cost
    'mid-range': 1.5,    # 50% more expensive
    'premium': 2.5       # 150% more expensive
}

# Severity multipliers
SEVERITY_MULTIPLIERS = {
    'low': 1.0,          # Base cost
    'medium': 1.8,       # 80% more expensive
    'high': 3.0          # 200% more expensive
}

def get_base_cost(damage_type, severity):
    """
    Get base repair cost from database
    
    Args:
        damage_type (str): Type of damage (dent, scratch, etc.)
        severity (str): Severity level (low, medium, high)
    
    Returns:
        float: Base cost for the damage type and severity
    """
    try:
        conn = sqlite3.connect('database/car_damage.db')
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT base_cost FROM cost_matrix WHERE damage_type = ? AND severity = ?',
            (damage_type.lower(), severity.lower())
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        else:
            # Fallback costs if not found in database
            fallback_costs = {
                ('dent', 'low'): 150.0,
                ('dent', 'medium'): 300.0,
                ('dent', 'high'): 600.0,
                ('scratch', 'low'): 100.0,
                ('scratch', 'medium'): 250.0,
                ('scratch', 'high'): 500.0,
                ('crack', 'low'): 200.0,
                ('crack', 'medium'): 400.0,
                ('crack', 'high'): 800.0,
                ('broken_glass', 'low'): 300.0,
                ('broken_glass', 'medium'): 500.0,
                ('broken_glass', 'high'): 1000.0,
                ('rust', 'low'): 120.0,
                ('rust', 'medium'): 280.0,
                ('rust', 'high'): 550.0,
            }
            return fallback_costs.get((damage_type.lower(), severity.lower()), 200.0)
            
    except Exception as e:
        print(f"Error getting base cost: {e}")
        return 200.0  # Default fallback cost

def estimate_repair_cost(car_category, damage_type, severity):
    """
    Calculate estimated repair cost based on all factors
    
    Args:
        car_category (str): Car category (economy, mid-range, premium)
        damage_type (str): Type of damage detected
        severity (str): Severity level of damage
    
    Returns:
        float: Estimated repair cost in USD
    """
    # Get base cost for damage type and severity
    base_cost = get_base_cost(damage_type, severity)
    
    # Get category multiplier
    category_multiplier = CAR_CATEGORY_MULTIPLIERS.get(car_category.lower(), 1.0)
    
    # Get severity multiplier (already factored in base cost, but we can add extra logic)
    severity_multiplier = SEVERITY_MULTIPLIERS.get(severity.lower(), 1.0)
    
    # Calculate final cost
    # Base cost already includes severity, so we mainly apply category multiplier
    estimated_cost = base_cost * category_multiplier
    
    # Round to 2 decimal places
    return round(estimated_cost, 2)

def get_cost_breakdown(car_category, damage_type, severity):
    """
    Get detailed cost breakdown for transparency
    
    Args:
        car_category (str): Car category
        damage_type (str): Type of damage
        severity (str): Severity level
    
    Returns:
        dict: Detailed cost breakdown
    """
    base_cost = get_base_cost(damage_type, severity)
    category_multiplier = CAR_CATEGORY_MULTIPLIERS.get(car_category.lower(), 1.0)
    final_cost = estimate_repair_cost(car_category, damage_type, severity)
    
    return {
        'base_cost': base_cost,
        'car_category': car_category,
        'category_multiplier': category_multiplier,
        'damage_type': damage_type,
        'severity': severity,
        'final_cost': final_cost,
        'breakdown': {
            'base_repair_cost': base_cost,
            'category_adjustment': f"{category_multiplier}x",
            'total_estimated_cost': final_cost
        }
    }

def get_cost_range(car_category, damage_type):
    """
    Get cost range for a damage type across all severity levels
    
    Args:
        car_category (str): Car category
        damage_type (str): Type of damage
    
    Returns:
        dict: Min and max cost estimates
    """
    low_cost = estimate_repair_cost(car_category, damage_type, 'low')
    medium_cost = estimate_repair_cost(car_category, damage_type, 'medium')
    high_cost = estimate_repair_cost(car_category, damage_type, 'high')
    
    return {
        'min_cost': low_cost,
        'max_cost': high_cost,
        'severity_costs': {
            'low': low_cost,
            'medium': medium_cost,
            'high': high_cost
        }
    }