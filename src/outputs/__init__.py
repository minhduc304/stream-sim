import logging
from typing import Dict, Any

from .stdout import StdoutConnector
from .file import FileConnector
from .kafka import KafkaConnector
from .http import HttpConnector
from .mqtt import MqttConnector

logger = logging.getLogger(__name__)

# Registry of output connector types
CONNECTOR_TYPES = {
    "stdout": StdoutConnector,
    "file": FileConnector,
    "kafka": KafkaConnector,
    "http": HttpConnector,
    "mqtt": MqttConnector,
}

def create_output_connector(config: Dict[str, Any]):
    """
    Create an output connector based on configuration.
    """
    connector_type = config.get("type")
    
    if connector_type in CONNECTOR_TYPES:
        return CONNECTOR_TYPES[connector_type](config)
    else:
        logger.warning(f"Unknown output type: {connector_type}, falling back to stdout")
        return StdoutConnector(config)