"""
Registry for data generator functions.
"""
import logging
from typing import Dict, Any, Callable, Optional, Awaitable

from .basic import (
    static_generator,
    random_int_generator,
    random_float_generator, 
    sequence_generator,
    timestamp_generator,
    choice_generator,
    uuid_generator,
    gaussian_generator,
    dependent_generator
)


# Type hint for generator functions
GeneratorFunc = Callable[..., Awaitable[Any]]


class GeneratorRegistry:
    """Registry of available data generator functions."""
    
    def __init__(self):
        """Initialize the generator registry with built-in generators."""
        self.logger = logging.getLogger("generators.registry")
        self._generators = {}
        
        # Register built-in generators
        self.register("static", static_generator)
        self.register("random_int", random_int_generator)
        self.register("random_float", random_float_generator)
        self.register("sequence", sequence_generator)
        self.register("timestamp", timestamp_generator)
        self.register("choice", choice_generator)
        self.register("uuid", uuid_generator)
        self.register("gaussian", gaussian_generator)
        self.register("dependent", dependent_generator)
        
        self.logger.info(f"Initialized generator registry with {len(self._generators)} generators")
    
    def register(self, name: str, generator_func: GeneratorFunc) -> None:
        """Register a new generator function."""
        if name in self._generators:
            self.logger.warning(f"Overriding existing generator: {name}")
        
        self._generators[name] = generator_func
        self.logger.debug(f"Registered generator: {name}")
    
    def get_generator(self, name: str) -> GeneratorFunc:
        """Get a generator function by name."""
        if name not in self._generators:
            self.logger.error(f"Generator not found: {name}")
            raise KeyError(f"Generator not found: {name}")
        
        return self._generators[name]
    
    def list_generators(self) -> list:
        """Get a list of all registered generator names."""
        return list(self._generators.keys())