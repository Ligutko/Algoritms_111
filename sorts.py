"""
Sorting algorithms module for DSA laboratory work.

Contains implementations of Selection Sort and Quick Sort algorithms
with strict type hinting and detailed documentation.
"""

from typing import List


def selection_sort(arr: List[int]) -> List[int]:
    """
    Sort an array using the Selection Sort algorithm.
    
    Selection Sort works by repeatedly finding the minimum element from the
    unsorted portion of the array and placing it at the beginning.
    
    Algorithm:
        1. Find the minimum element in the unsorted portion
        2. Swap it with the first element of the unsorted portion
        3. Move the boundary between sorted and unsorted portions
        4. Repeat until the entire array is sorted
    
    Args:
        arr: A list of integers to be sorted.
        
    Returns:
        The sorted list of integers.
        
    Time Complexity:
        Best case: O(n²)
        Average case: O(n²)
        Worst case: O(n²)
        
    Space Complexity:
        O(1) - sorts in-place
        
    Example:
        >>> selection_sort([64, 34, 25, 12, 22, 11, 90])
        [11, 12, 22, 25, 34, 64, 90]
    """
    n = len(arr)
    
    # Traverse through all array elements
    for i in range(n):
        # Find the minimum element in the remaining unsorted portion
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # Swap the found minimum element with the first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr


def _partition(arr: List[int], low: int, high: int) -> int:
    """
    Helper function for Quick Sort that partitions the array.
    
    Selects a pivot element and partitions the array such that:
    - All elements less than the pivot are on the left
    - All elements greater than the pivot are on the right
    
    This function uses the last element as the pivot.
    
    Args:
        arr: The list being partitioned.
        low: The starting index of the partition.
        high: The ending index of the partition.
        
    Returns:
        The index of the pivot after partitioning.
    """
    # Choose the last element as pivot
    pivot = arr[high]
    
    # Index of the smaller element - indicates the right position
    # of pivot found so far
    i = low - 1
    
    # Traverse through all elements
    # Compare each element with pivot
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # Swap the pivot to its correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(arr: List[int]) -> List[int]:
    """
    Sort an array using the Quick Sort algorithm with Divide and Conquer.

    Quick Sort is a highly efficient divide-and-conquer sorting algorithm that works by:
    1. Selecting a pivot element from the array
    2. Partitioning the array around the pivot
    ============================================================
      Розділ 3: Реалізація алгоритмів сортування
    ============================================================
    
      Початковий масив : [143, 8275, 1774, 8404, 354, 7226, 463, 3640, 6453, 2218]
    
      Selection Sort   : [143, 354, 463, 1774, 2218, 3640, 6453, 7226, 8275, 8404]
      Quick Sort       : [143, 354, 463, 1774, 2218, 3640, 6453, 7226, 8275, 8404]
    
      Результати збігаються : ✅ ТАК
    
    ============================================================    3. Iteratively processing the left and right sub-arrays via an explicit stack

    This implementation uses an explicit stack instead of Python recursion to
    avoid hitting Python's default recursion limit on large or adversarial
    inputs (e.g. already-sorted / reversed arrays of 10 000+ elements).

    Args:
        arr: A list of integers to be sorted.

    Returns:
        The sorted list of integers (in-place).

    Time Complexity:
        Best case:    O(n log n) - balanced partitions
        Average case: O(n log n)
        Worst case:   O(n²)     - pivot is always the smallest/largest element

    Space Complexity:
        O(log n) average - explicit stack depth mirrors recursion depth

    Example:
        >>> quick_sort([64, 34, 25, 12, 22, 11, 90])
        [11, 12, 22, 25, 34, 64, 90]
    """
    if len(arr) <= 1:
        return arr

    # Explicit stack stores (low, high) pairs to process
    stack: List[tuple] = [(0, len(arr) - 1)]

    while stack:
        low, high = stack.pop()
        if low < high:
            pi = _partition(arr, low, high)
            # Push both sub-arrays onto the stack
            stack.append((low, pi - 1))
            stack.append((pi + 1, high))

    return arr
