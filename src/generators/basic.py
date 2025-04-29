"""
Basic generator functions for data fields.
"""
import random
import uuid
import datetime
from typing import Dict, Any, List, Optional, Union, Callable
import asyncio
import logging

logger = logging.getLogger("generators.basic")

# Type aliases
StateDict = Dict[str, Any]
RecordDict = Dict[str, Any]


async def static_generator(
    value: Any, 
    state: Optional[StateDict] = None, 
    record: Optional[RecordDict] = None, 
    **kwargs
) -> Any:
    """Generate a static value."""
    return value


async def random_int_generator(
    min_val: int = 0, 
    max_val: int = 100, 
    state: Optional[StateDict] = None, 
    record: Optional[RecordDict] = None, 
    **kwargs
) -> int:
    """Generate a random integer"""
    return random.randint(min_val, max_val)


async def random_float_generator(
    min_val: float = 0.0, 
    max_val: float = 1.0, 
    precision: int = 4, 
    state: Optional[StateDict] = None, 
    record: Optional[RecordDict] = None, 
    **kwargs
) -> float:
    """Generate a random float"""
    value = random.uniform(min_val, max_val)
    return round(value, precision)


async def sequence_generator(
    start: int = 0, 
    step: int = 1, 
    state_key: str = "_sequence", 
    state: Optional[StateDict] = None, 
    record: Optional[RecordDict] = None, 
    **kwargs
) -> int:
    """Generate a sequence of integers.
    """
    if state is None:
        state = {}
    
    # Initialize sequence if not exists
    full_key = f"{state_key}"
    if full_key not in state:
        state[full_key] = start
        return start
    
    # Get current value and update for next time
    current = state[full_key]
    state[full_key] += step
    return current


async def timestamp_generator(
    format: str = "iso", 
    timezone: str = "utc", 
    state: Optional[StateDict] = None, 
    record: Optional[RecordDict] = None, 
    **kwargs
) -> Union[str, int]:
    """Generate a timestamp. """
    now = datetime.datetime.now(datetime.timezone.utc)
    
    if format == "epoch":
        return int(now.timestamp())
    elif format == "iso":
        return now.isoformat()
    else:
        # Custom format
        try:
            return now.strftime(format)
        except ValueError as e:
            logger.error(f"Invalid timestamp format: {format}, using ISO8601")
            return now.isoformat()


async def choice_generator(
    values: List[Any],
    weights: Optional[List[float]] = None,
    state: Optional[StateDict] = None, 
    record: Optional[RecordDict] = None, 
    **kwargs
) -> Any:
    """Generate a value from a list of choices."""
    return random.choices(values, weights=weights, k=1)[0]


async def uuid_generator(
    state: Optional[StateDict] = None, 
    record: Optional[RecordDict] = None, 
    **kwargs
) -> str:
    """Generate a UUID."""
    return str(uuid.uuid4())


async def gaussian_generator(
    mean: float = 0.0, 
    stddev: float = 1.0, 
    precision: int = 4, 
    state: Optional[StateDict] = None, 
    record: Optional[RecordDict] = None, 
    **kwargs
) -> float:
    """Generate a value from a Gaussian distribution.
    """
    value = random.gauss(mean, stddev)
    return round(value, precision)


async def dependent_generator(
    field: str,
    func: Union[str, Callable],
    state: Optional[StateDict] = None, 
    record: Optional[RecordDict] = None, 
    **kwargs
) -> Any:
    """Generate a value dependent on another field.
    """
    if record is None or field not in record:
        logger.error(f"Dependent field not found: {field}")
        return None
    
    source_value = record[field]
    
    if isinstance(func, str):
        # Convert string to function (use with caution!)
        try:
            func_obj = eval(func)
            return func_obj(source_value)
        except Exception as e:
            logger.error(f"Error evaluating function '{func}': {e}")
            return None
    else:
        # Assume func is callable
        return func(source_value)