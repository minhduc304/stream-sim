"""
Configuration loading and validation for the data stream simulator.
"""
import logging
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional


class ValidationError(Exception):
    """Exception raised for configuration validation errors."""
    pass


class SimulationConfig:
    """Parsed and validated simulation configuration."""
    
    def __init__(self, config_dict: Dict[str, Any]):
        self.raw_config = config_dict
        self.streams = self._extract_streams(config_dict)
        self.global_config = config_dict.get("global", {})
    
    def _extract_streams(self, config: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Extract stream configurations from the raw config."""
        streams = {}
        
        # If there's a streams key, use those configurations
        if "streams" in config:
            for stream_id, stream_config in config["streams"].items():
                # Apply global defaults if they exist
                if "global" in config:
                    merged_config = self._merge_configs(config["global"], stream_config)
                else:
                    merged_config = stream_config
                streams[stream_id] = merged_config
        else:
            # If no streams key, assume the whole config is for a single stream
            # Remove global config if it exists to avoid confusion
            single_config = config.copy()
            if "global" in single_config:
                global_config = single_config.pop("global")
                # Apply global defaults to the single stream
                single_config = self._merge_configs(global_config, single_config)
            streams["default"] = single_config
        
        return streams
    
    @staticmethod
    def _merge_configs(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Merge two configuration dictionaries with override taking precedence."""
        result = base.copy()
        
        for key, override_value in override.items():
            # If both configs have this key and both values are dicts, do a deep merge
            if key in result and isinstance(result[key], dict) and isinstance(override_value, dict):
                result[key] = SimulationConfig._merge_configs(result[key], override_value)
            # Otherwise, override the value
            else:
                result[key] = override_value
        
        return result


class ConfigLoader:
    """Loads and validates configuration from YAML or JSON files."""
    
    def __init__(self):
        self.logger = logging.getLogger("config.loader")
    
    def load(self, config_path: Path) -> SimulationConfig:
        """Load configuration from a file."""
        self.logger.info(f"Loading configuration from: {config_path}")
        
        # Load raw configuration
        raw_config = self._load_yaml_or_json(config_path)
        
        # Validate configuration
        self._validate_config(raw_config)
        
        # Parse into SimulationConfig
        return SimulationConfig(raw_config)
    
    def _load_yaml_or_json(self, path: Path) -> Dict[str, Any]:
        """Load YAML or JSON file based on extension."""
        if path.suffix.lower() in (".yaml", ".yml"):
            with open(path, "r") as f:
                return yaml.safe_load(f)
        elif path.suffix.lower() == ".json":
            import json
            with open(path, "r") as f:
                return json.load(f)
        else:
            raise ValueError(f"Unsupported configuration file format: {path.suffix}")
    
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """Basic validation of configuration structure.
        
        This validates the overall structure, but not the specific field types/values.
        Detailed validation should happen in the components that use each part.
        """
        # Check if streams are defined
        if "streams" in config:
            # Multi-stream configuration
            if not isinstance(config["streams"], dict):
                raise ValidationError("'streams' must be a dictionary")
            
            # Check each stream
            for stream_id, stream_config in config["streams"].items():
                self._validate_stream_config(stream_id, stream_config)
        else:
            # Single stream configuration
            # Remove global config for validation if it exists
            stream_config = {k: v for k, v in config.items() if k != "global"}
            self._validate_stream_config("default", stream_config)
    
    def _validate_stream_config(self, stream_id: str, config: Dict[str, Any]) -> None:
        """Validate a single stream configuration."""
        # Check required fields
        if "schema" not in config:
            raise ValidationError(f"Stream '{stream_id}' is missing required 'schema' field")
            
        if not isinstance(config["schema"], dict):
            raise ValidationError(f"Stream '{stream_id}': 'schema' must be a dictionary")
            
        # Basic schema validation
        for field_name, field_config in config["schema"].items():
            if not isinstance(field_config, dict):
                raise ValidationError(f"Field '{field_name}' in stream '{stream_id}' must be a dictionary")