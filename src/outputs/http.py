import logging
import asyncio
import aiohttp
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class HttpConnector:
    """
    Output connector that sends data to an HTTP endpoint.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the HTTP connector.
        
        Args:
            config: Output configuration
        """
        self.config = config
        self.url = config.get("url", "http://localhost:8000")
        self.method = config.get("method", "POST").upper()
        self.headers = config.get("headers", {"Content-Type": "application/json"})
        self.session = None
        
        # Create aiohttp session
        self._create_session()
    
    def _create_session(self) -> None:
        """
        Create aiohttp session.
        """
        try:
            self.session = aiohttp.ClientSession(headers=self.headers)
            logger.info(f"Created HTTP session for endpoint: {self.url}")
        except Exception as e:
            logger.error(f"Error creating HTTP session: {e}")
    
    async def send(self, data: str) -> None:
        """
        Send data to HTTP endpoint.
        
        Args:
            data: Formatted data to send
        """
        if self.session is None:
            logger.error("HTTP session not initialized")
            return
        
        try:
            # Send the request
            if self.method == "GET":
                async with self.session.get(self.url, params={"data": data}) as response:
                    await response.text()
            else:  # Default to POST
                async with self.session.post(self.url, data=data) as response:
                    await response.text()
            
            logger.debug(f"Sent HTTP {self.method} request to {self.url}")
        except Exception as e:
            logger.error(f"Error sending HTTP request: {e}")
    
    async def close(self) -> None:
        """
        Close the aiohttp session.
        """
        if self.session is not None:
            try:
                await self.session.close()
                logger.info("Closed HTTP session")
            except Exception as e:
                logger.error(f"Error closing HTTP session: {e}")
            
            self.session = None
    
    def __del__(self):
        """
        Ensure the session is closed when the connector is destroyed.
        """
        if self.session is not None and not self.session.closed:
            logger.warning("HTTP session was not properly closed")