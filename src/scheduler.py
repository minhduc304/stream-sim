import asyncio
import logging
import time
from typing import Dict, Any, List, Callable, Union, Optional
import random

from .generators import create_record
from .state import StateManager
from .formatters import format_record
from .outputs import create_output_connector
from .events import check_events

logger = logging.getLogger(__name__)

class Scheduler:
    """
    Manages the timing and execution of data generation and output.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the scheduler.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.state_managers = {}
        self.output_connectors = {}
        self.running = False
        
        # Initialize state managers for each stream
        for stream_name, stream_config in config["streams"].items():
            initial_state = stream_config.get("initial_state", {})
            self.state_managers[stream_name] = StateManager(initial_state)
            
            # Initialize output connectors for each stream
            self.output_connectors[stream_name] = []
            for output_config in stream_config["outputs"]:
                connector = create_output_connector(output_config)
                self.output_connectors[stream_name].append(connector)
    
    async def run(self):
        """
        Run the simulation.
        """
        self.running = True
        
        # Create tasks for each stream
        tasks = []
        for stream_name, stream_config in self.config["streams"].items():
            task = asyncio.create_task(
                self._run_stream(stream_name, stream_config)
            )
            tasks.append(task)
        
        logger.info(f"Starting {len(tasks)} simulation streams")
        
        # Wait for all tasks to complete (or for cancellation)
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            logger.info("Simulation cancelled")
            self.running = False
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _run_stream(self, stream_name: str, stream_config: Dict[str, Any]):
        """
        Run a single simulation stream.
        
        Args:
            stream_name: Name of the stream
            stream_config: Configuration for the stream
        """
        logger.info(f"Starting stream: {stream_name}")
        state_manager = self.state_managers[stream_name]
        
        # Calculate the time between records
        rate = stream_config["rate"]  # records per second
        base_interval = 1.0 / rate
        
        # Get optional jitter configuration
        jitter = stream_config.get("jitter", 0.0)  # Default: no jitter
        
        # Count for sequence tracking
        record_count = 0
        
        while self.running:
            start_time = time.time()
            
            try:
                # Generate a record
                record_count += 1
                
                # Check if we should inject an event
                events = stream_config.get("events", [])
                event_record = None
                if events:
                    event_record = check_events(events, record_count, state_manager.state)
                
                if event_record is not None:
                    record = event_record
                    logger.debug(f"[{stream_name}] Injecting event: {record}")
                else:
                    # Generate a normal record
                    record = create_record(
                        stream_config["schema"],
                        state_manager.state,
                        record_count
                    )
                    logger.debug(f"[{stream_name}] Generated record: {record}")
                
                # Update state if needed
                state_manager.update(record)
                
                # Format and send the record to all outputs
                for connector in self.output_connectors[stream_name]:
                    output_format = connector.config["format"]
                    formatted_record = format_record(record, output_format)
                    await connector.send(formatted_record)
                
                # Calculate time to sleep
                if jitter > 0:
                    # Add random jitter within the specified range
                    interval = base_interval * (1 + random.uniform(-jitter, jitter))
                else:
                    interval = base_interval
                
                elapsed = time.time() - start_time
                sleep_time = max(0, interval - elapsed)
                
                # Sleep until next record
                await asyncio.sleep(sleep_time)
                
            except Exception as e:
                logger.error(f"Error in stream {stream_name}: {e}")
                # Continue with next record
                await asyncio.sleep(base_interval)