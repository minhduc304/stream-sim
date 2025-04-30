import datetime
from typing import Dict, Any, Union

def generate_timestamp(config: Dict[str, Any], state: Dict[str, Any], count: int) -> Union[str, int]:
    """
    Generate a timestamp.
    """
    timestamp_format = config.get("format", "iso")
    timestamp_type = config.get("type", "utc")
    
    # Get current time
    if timestamp_type == "utc":
        now = datetime.datetime.now(datetime.timezone.utc)
    else:
        now = datetime.datetime.now()
    
    # Apply optional offset
    if "offset" in config:
        offset = config["offset"]
        if isinstance(offset, dict):
            seconds = offset.get("seconds", 0)
            minutes = offset.get("minutes", 0)
            hours = offset.get("hours", 0)
            days = offset.get("days", 0)
            
            delta = datetime.timedelta(
                seconds=seconds,
                minutes=minutes,
                hours=hours,
                days=days
            )
            
            now = now + delta
    
    # Format the timestamp
    if timestamp_format == "iso":
        return now.isoformat()
    elif timestamp_format == "epoch":
        return int(now.timestamp())
    elif timestamp_format == "custom":
        custom_format = config.get("custom_format", "%Y-%m-%d %H:%M:%S")
        return now.strftime(custom_format)
    else:
        return now.isoformat()

# data_stream_simulator/generators/stateful.py
"""
Stateful data generation functions for the Data Stream Simulator.
"""
import logging
from typing import Dict, Any, Callable

logger = logging.getLogger(__name__)

def generate_dependent(config: Dict[str, Any], state: Dict[str, Any], count: int, record: Dict[str, Any]) -> Any:
    """
    Generate a value dependent on another field in the same record.
    
    Args:
        config: Generator configuration
        state: Current state
        count: Current record count
        record: Current record (partially filled)
        
    Returns:
        Dependent value
    """
    field_name = config.get("field")
    
    if not field_name or field_name not in record:
        logger.warning(f"Dependent field not found: {field_name}")
        return None
    
    source_value = record[field_name]
    
    # Apply transformation function if provided
    if "func" in config:
        func_str = config["func"]
        try:
            # Simple but unsafe eval - in production, use safer alternatives
            func = eval(func_str)
            return func(source_value)
        except Exception as e:
            logger.error(f"Error evaluating dependent function: {e}")
            return None
    
    # If no function provided, just return the source value
    return source_value

def generate_stateful(config: Dict[str, Any], state: Dict[str, Any], count: int) -> Any:
    """
    Generate a value based on state.
    """
    state_key = config.get("state_key", "_default_stateful")
    
    # Initialize state if needed
    if state_key not in state:
        state[state_key] = config.get("initial", 0)
    
    # Get the current state value
    current_value = state[state_key]
    
    # Apply update function if provided
    if "update_func" in config:
        func_str = config["update_func"]
        try:
            # Simple but unsafe eval - in production, use safer alternatives
            func = eval(func_str)
            state[state_key] = func(current_value, count)
        except Exception as e:
            logger.error(f"Error evaluating stateful update function: {e}")
    
    return current_value
