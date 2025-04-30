import sys
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class StdoutConnector:
    """
    Output connector that prints to standard output.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the stdout connector.
        """
        self.config = config
    
    async def send(self, data: str) -> None:
        """
        Send data to stdout.
        """
        print(data, flush=True)
