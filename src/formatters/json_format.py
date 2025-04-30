import json
from typing import Dict, Any

def format_json(record: Dict[str, Any]) -> str:
    """
    Format a record as JSON.
    """
    return json.dumps(record)