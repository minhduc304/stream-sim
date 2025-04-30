import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Lazy import Faker to avoid dependency issues if not used
_faker = None

def _get_faker():
    """
    Get or initialize the Faker instance.
    """
    global _faker
    if _faker is None:
        try:
            from faker import Faker
            _faker = Faker()
        except ImportError:
            logger.warning("Faker library not installed. Install with: pip install faker")
            return None
    
    return _faker

def generate_faker(config: Dict[str, Any], state: Dict[str, Any], count: int) -> Optional[str]:
    """
    Generate data using the Faker library.
    """
    faker = _get_faker()
    if faker is None:
        return None
    
    faker_type = config.get("type", "name")
    
    # Get the faker provider method
    faker_method = getattr(faker, faker_type, None)
    
    if faker_method is None:
        logger.warning(f"Unknown Faker type: {faker_type}")
        return None
    
    try:
        # Pass any additional parameters to the Faker method
        params = {k: v for k, v in config.items() if k not in ["type"]}
        return faker_method(**params)
    except Exception as e:
        logger.error(f"Error generating fake data: {e}")
        return None