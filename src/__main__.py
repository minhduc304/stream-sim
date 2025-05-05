"""
Command-line interface for the Stream Sim.
"""
import argparse
import asyncio
import logging
import sys
from pathlib import Path

from .config import load_config
from .scheduler import Scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("stream-sim")

def parse_args():
    parser = argparse.ArgumentParser(description="Stream Sim")
    parser.add_argument("--config", "-c", required=True, help="Path to configuration file")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()

def main():
    args = parse_args()
    
    if args.debug:
        logger.setLevel(logging.DEBUG)
    
    config_path = Path(args.config)
    if not config_path.exists():
        logger.error(f"Configuration file not found: {args.config}")
        sys.exit(1)
    
    try:
        config = load_config(config_path)
        logger.info(f"Loaded configuration from {config_path}")
        logger.debug(f"Configuration: {config}")
        
        scheduler = Scheduler(config)
        asyncio.run(scheduler.run())
    except Exception as e:
        logger.exception(f"Error running simulator: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()