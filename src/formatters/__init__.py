import logging
from typing import Dict, Any, Union

from .json_format import format_json
from .csv_format import format_csv

logger = logging.getLogger(__name__)

# Registry of formatters
FORMATTERS = {
    "json": format_json,
    "csv": format_csv,
}

def format_record(record: Dict[str, Any], output_format: str) -> str:
    """
    Format a record for output.
    """
    if output_format in FORMATTERS:
        return FORMATTERS[output_format](record)
    else:
        logger.warning(f"Unknown format: {output_format}, falling back to json")
        return FORMATTERS["json"](record)