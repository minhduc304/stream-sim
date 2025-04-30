import logging
import yaml
from pathlib import Path
from typing import Dict, Any, List, Union, Optional

logger = logging.getLogger(__name__)

def load_config(config_path: Path) -> Dict[str, Any]:
    """Load a configuration from a YAML file."""
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    # Validate the configuration
    validate_config(config)
    
    return config

def validate_config(config: Dict[str, Any]) -> None:
    """Validate the configuration structure."""
    # Check for required top-level keys
    required_keys = ["streams"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")
    
    # Validate each stream
    for stream_name, stream_config in config["streams"].items():
        validate_stream_config(stream_name, stream_config)

def validate_stream_config(stream_name: str, stream_config: Dict[str, Any]) -> None:
    """Validate a single stream configuration."""
    required_keys = ["schema", "rate", "outputs"]
    for key in required_keys:
        if key not in stream_config:
            raise ValueError(f"Stream '{stream_name}' missing required key: {key}")
    
    # Validate schema
    if not isinstance(stream_config["schema"], dict):
        raise ValueError(f"Stream '{stream_name}' schema must be a dictionary")
    
    # Validate rate
    if not isinstance(stream_config["rate"], (int, float)) or stream_config["rate"] <= 0:
        raise ValueError(f"Stream '{stream_name}' rate must be a positive number")
    
    # Validate outputs
    if not isinstance(stream_config["outputs"], list) or not stream_config["outputs"]:
        raise ValueError(f"Stream '{stream_name}' outputs must be a non-empty list")
    
    # Validate each output
    for i, output in enumerate(stream_config["outputs"]):
        if not isinstance(output, dict):
            raise ValueError(f"Stream '{stream_name}' output {i} must be a dictionary")
        if "type" not in output:
            raise ValueError(f"Stream '{stream_name}' output {i} missing required key: type")
        if "format" not in output:
            raise ValueError(f"Stream '{stream_name}' output {i} missing required key: format")
