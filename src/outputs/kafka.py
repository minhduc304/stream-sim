import logging
import asyncio
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class KafkaConnector:
    """
    Output connector that sends to a Kafka topic.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Kafka connector.
        """
        self.config = config
        self.producer = None
        self.topic = config.get("topic", "data-stream")
        self.bootstrap_servers = config.get("bootstrap_servers", "localhost:9092")
        
        # Lazy initialization of Kafka producer
        self._initialize_producer()
    
    def _initialize_producer(self) -> None:
        """
        Initialize the Kafka producer.
        """
        try:
            from kafka import KafkaProducer
            
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda x: x.encode("utf-8")
            )
            
            logger.info(f"Connected to Kafka bootstrap servers: {self.bootstrap_servers}")
        except ImportError:
            logger.warning("Kafka-python not installed. Install with: pip install kafka-python")
        except Exception as e:
            logger.error(f"Error connecting to Kafka: {e}")
    
    async def send(self, data: str) -> None:
        """
        Send data to Kafka topic.
        """
        if self.producer is None:
            logger.error("Kafka producer not initialized")
            return
        
        try:
            # Send the data asynchronously
            future = self.producer.send(self.topic, data)
            
            # Handle the result
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, future.get, 10)  # 10 second timeout
            
            logger.debug(f"Sent message to Kafka topic: {self.topic}")
        except Exception as e:
            logger.error(f"Error sending to Kafka: {e}")
    
    def __del__(self):
        """
        Close the producer when the connector is destroyed.
        """
        if self.producer is not None:
            try:
                self.producer.close()
                logger.info("Closed Kafka producer")
            except Exception as e:
                logger.error(f"Error closing Kafka producer: {e}")
