import os
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional, TextIO

logger = logging.getLogger(__name__)

class FileConnector:
    """
    Output connector that writes to a file.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the file connector.
        """
        self.config = config
        self.filename = config.get("filename", "output.txt")
        self.append = config.get("append", True)
        self.file_handle = None
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Open the file
        mode = "a" if self.append else "w"
        self.file_handle = open(self.filename, mode, encoding="utf-8")
        
        logger.info(f"Opened file for output: {self.filename}")
    
    async def send(self, data: str) -> None:
        """
        Write data to the file.
        """
        if self.file_handle is None:
            logger.error("File handle is closed")
            return
        
        try:
            # Write the data
            self.file_handle.write(data + "\n")
            self.file_handle.flush()
        except Exception as e:
            logger.error(f"Error writing to file: {e}")
    
    def __del__(self):
        """
        Close the file when the connector is destroyed.
        """
        if self.file_handle is not None:
            try:
                self.file_handle.close()
                logger.info(f"Closed file: {self.filename}")
            except Exception as e:
                logger.error(f"Error closing file: {e}")
            
            self.file_handle = None
