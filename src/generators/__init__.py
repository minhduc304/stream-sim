import logging
from typing import Dict, Any, Callable, List

from .basic import (
    generate_static,
    generate_random_int,
    generate_random_float,
    generate_sequence_int,
    generate_choice,
    generate_uuid,
    generate_gaussian
)
from .datetime import generate_timestamp
from .stateful import generate_dependent, generate_stateful
from .faker import generate_faker

logger = logging.getLogger(__name__)

# Registry of generator functions
GENERATORS = {
    "static": generate_static,
    "random_int": generate_random_int,
    "random_float": generate_random_float,
    "sequence_int": generate_sequence_int,
    "choice": generate_choice,
    "uuid": generate_uuid,
    "timestamp": generate_timestamp,
    "gaussian": generate_gaussian,
    "faker": generate_faker,
    "dependent": generate_dependent,
    "stateful": generate_stateful,
}

def create_record(schema: Dict[str, Any], state: Dict[str, Any], count: int) -> Dict[str, Any]:
    """
    Generate a complete record based on the schema.
    """
    record = {}
    
    # First pass: Generate all non-dependent fields
    for field_name, field_config in schema.items():
        if isinstance(field_config, dict) and "type" in field_config:
            # If field depends on other fields, skip for now
            if field_config["type"] == "dependent":
                continue
                
            # Generate the field value
            generator_type = field_config["type"]
            if generator_type in GENERATORS:
                try:
                    record[field_name] = GENERATORS[generator_type](field_config, state, count)
                except Exception as e:
                    logger.error(f"Error generating field {field_name}: {e}")
                    record[field_name] = None
            else:
                logger.warning(f"Unknown generator type: {generator_type}")
                record[field_name] = None
        else:
            # Simple static value
            record[field_name] = field_config
    
    # Second pass: Generate dependent fields
    for field_name, field_config in schema.items():
        if isinstance(field_config, dict) and field_config.get("type") == "dependent":
            try:
                record[field_name] = generate_dependent(field_config, state, count, record)
            except Exception as e:
                logger.error(f"Error generating dependent field {field_name}: {e}")
                record[field_name] = None
    
    return record
