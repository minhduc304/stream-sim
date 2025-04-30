import logging
import random
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

def check_events(events: List[Dict[str, Any]], record_count: int, state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Check if an event should be injected based on triggers."""
    for event in events:
        if _check_event_trigger(event, record_count, state):
            # Clone the event record to avoid modifying the original
            return event["record"].copy()
    
    return None

def _check_event_trigger(event: Dict[str, Any], record_count: int, state: Dict[str, Any]) -> bool:
    """Check if a single event trigger fires."""
    # Handle count-based triggers
    if "at_count" in event:
        if record_count == event["at_count"]:
            return True
    
    if "every_count" in event:
        if record_count % event["every_count"] == 0:
            return True
    
    # Handle probability-based triggers
    if "probability" in event:
        if random.random() < event["probability"]:
            return True
    
    # More trigger types could be added here
    
    return False