import random
import uuid
from typing import Dict, Any, Union, List, Optional

def generate_static(config: Dict[str, Any], state: Dict[str, Any], count: int) -> Any:
    """
    Generate a static value.
    
    Args:
        config: Generator configuration
        state: Current state
        count: Current record count
        
    Returns:
        Static value
    """
    return config.get("value")

def generate_random_int(config: Dict[str, Any], state: Dict[str, Any], count: int) -> int:
    """
    Generate a random integer.
    
    Args:
        config: Generator configuration
        state: Current state
        count: Current record count
        
    Returns:
        Random integer
    """
    min_val = config.get("min", 0)
    max_val = config.get("max", 100)
    return random.randint(min_val, max_val)

def generate_random_float(config: Dict[str, Any], state: Dict[str, Any], count: int) -> float:
    """
    Generate a random float.
    
    Args:
        config: Generator configuration
        state: Current state
        count: Current record count
        
    Returns:
        Random float
    """
    min_val = config.get("min", 0.0)
    max_val = config.get("max", 1.0)
    precision = config.get("precision", 4)
    
    value = random.uniform(min_val, max_val)
    return round(value, precision)

def generate_sequence_int(config: Dict[str, Any], state: Dict[str, Any], count: int) -> int:
    """
    Generate a sequence integer.
    
    Args:
        config: Generator configuration
        state: Current state
        count: Current record count
        
    Returns:
        Sequence integer
    """
    # Get the sequence parameters
    start = config.get("start", 0)
    step = config.get("step", 1)
    
    # Get or create sequence state
    sequence_name = config.get("name", "_default")
    state_key = f"sequence_{sequence_name}"
    
    if state_key not in state:
        # Initialize the sequence
        state[state_key] = start
        return start
    
    # Get current value
    current = state[state_key]
    
    # Update state for next time
    state[state_key] = current + step
    
    return current

def generate_choice(config: Dict[str, Any], state: Dict[str, Any], count: int) -> Any:
    """
    Generate a value from a list of choices.
    
    Args:
        config: Generator configuration
        state: Current state
        count: Current record count
        
    Returns:
        Selected value
    """
    values = config.get("values", [])
    weights = config.get("weights", None)
    
    if not values:
        return None
    
    return random.choices(values, weights=weights, k=1)[0]

def generate_uuid(config: Dict[str, Any], state: Dict[str, Any], count: int) -> str:
    """
    Generate a UUID.
    
    Args:
        config: Generator configuration
        state: Current state
        count: Current record count
        
    Returns:
        UUID string
    """
    return str(uuid.uuid4())

def generate_gaussian(config: Dict[str, Any], state: Dict[str, Any], count: int) -> float:
    """
    Generate a value from a Gaussian (normal) distribution.
    
    Args:
        config: Generator configuration
        state: Current state
        count: Current record count
        
    Returns:
        Float from normal distribution
    """
    mean = config.get("mean", 0.0)
    stddev = config.get("stddev", 1.0)
    precision = config.get("precision", 4)
    
    value = random.normalvariate(mean, stddev)
    return round(value, precision)