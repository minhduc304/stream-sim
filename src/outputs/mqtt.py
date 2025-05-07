import logging
import asyncio
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class MqttConnector:
    """
    Output connector that publishes to an MQTT topic.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the MQTT connector.
        
        Args:
            config: Output configuration
        """
        self.config = config
        self.client = None
        self.topic = config.get("topic", "data-stream")
        self.broker = config.get("broker", "localhost")
        self.port = config.get("port", 1883)
        self.client_id = config.get("client_id", "data-simulator")
        self.qos = config.get("qos", 0)
        
        # Lazy initialization of MQTT client
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """
        Initialize the MQTT client.
        """
        try:
            import paho.mqtt.client as mqtt
            
            # Create client
            self.client = mqtt.Client(client_id=self.client_id)
            
            # Set username and password if provided
            if "username" in self.config and "password" in self.config:
                self.client.username_pw_set(
                    self.config["username"],
                    self.config["password"]
                )
            
            # Connect to broker
            self.client.connect(self.broker, self.port)
            
            # Start the loop in a separate thread
            self.client.loop_start()
            
            logger.info(f"Connected to MQTT broker: {self.broker}:{self.port}")
        except ImportError:
            logger.warning("Paho MQTT not installed. Install with: pip install paho-mqtt")
        except Exception as e:
            logger.error(f"Error connecting to MQTT broker: {e}")
    
    async def send(self, data: str) -> None:
        """
        Publish data to MQTT topic.
        
        Args:
            data: Formatted data to publish
        """
        if self.client is None:
            logger.error("MQTT client not initialized")
            return
        
        try:
            # Run the publish in the default executor
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self.client.publish,
                self.topic,
                data,
                self.qos
            )
            
            logger.debug(f"Published message to MQTT topic: {self.topic}")
        except Exception as e:
            logger.error(f"Error publishing to MQTT: {e}")
    
    def __del__(self):
        """
        Clean up resources when the connector is destroyed.
        """
        if self.client is not None:
            try:
                self.client.loop_stop()
                self.client.disconnect()
                logger.info("Disconnected from MQTT broker")
            except Exception as e:
                logger.error(f"Error disconnecting from MQTT broker: {e}")