"""
Utility module for DSA laboratory work.

Contains functions for array generation and execution timing.
"""

import random
import time
import functools
from typing import Callable, Dict, List, TypeVar, Any


# Type variable for decorator return type
F = TypeVar('F', bound=Callable[..., Any])


def generate_random_array(size: int) -> List[int]:
    """
    Generate an array of random integers.
    
    Args:
        size: The number of elements in the array.
        
    Returns:
        A list of random integers.
    """
    return [random.randint(1, 10000) for _ in range(size)]


def generate_nearly_sorted_array(size: int) -> List[int]:
    """
    Generate an array where ~90% of elements are sorted, and 10% are randomly swapped.
    
    Args:
        size: The number of elements in the array.
        
    Returns:
        A list with mostly sorted elements with some random swaps.
    """
    # Create a sorted array
    arr = list(range(1, size + 1))
    
    # Calculate number of elements to swap (10% of size)
    num_swaps = max(1, size // 10)
    
    # Randomly swap elements
    for _ in range(num_swaps):
        i, j = random.sample(range(size), 2)
        arr[i], arr[j] = arr[j], arr[i]
    
    return arr


def generate_reversed_array(size: int) -> List[int]:
    """
    Generate a strictly descending array.
    
    Args:
        size: The number of elements in the array.
        
    Returns:
        A list of integers in strictly descending order.
    """
    return list(range(size, 0, -1))


def generate_arrays() -> Dict[str, List[int]]:
    """
    Generate a dictionary of integer arrays with different sizes.
    
    Returns:
        A dictionary with keys representing array sizes and values as the arrays.
        Sizes: 10, 100, 1000, 10000.
    """
    sizes = [10, 100, 1000, 10000]
    return {
        f"array_{size}": generate_random_array(size)
        for size in sizes
    }


def time_it(func: F) -> F:
    """
    Decorator to measure and print the execution time of a function.
    
    This decorator wraps a function, measures its execution time in seconds
    with high precision, prints the time to the console, and returns the
    original function's result.
    
    Args:
        func: The function to be decorated.
        
    Returns:
        The decorated function that prints execution time.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Wrapper function that measures execution time."""
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        elapsed_time = end_time - start_time
        
        # Print execution time in a readable format
        if elapsed_time < 1e-3:
            print(f"⏱️ {func.__name__}() executed in {elapsed_time * 1e6:.2f} µs")
        elif elapsed_time < 1:
            print(f"⏱️ {func.__name__}() executed in {elapsed_time * 1e3:.2f} ms")
        else:
            print(f"⏱️ {func.__name__}() executed in {elapsed_time:.2f} s")
        
        return result
    
    return wrapper
