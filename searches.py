"""
Search algorithms module for DSA laboratory work.

Contains implementations of Linear Search and Interpolation Search algorithms
with strict type hinting and detailed documentation.
"""


def linear_search(arr: list[int], key: int) -> int:
    """
    Search for a key in an array using the Linear Search algorithm.

    Sequentially checks each element of the array until the key is found
    or the entire array has been traversed.

    Args:
        arr: A sorted or unsorted list of integers to search through.
        key: The integer value to search for.

    Returns:
        The index of the key if found, or -1 if not found.

    Time Complexity:
        Best case:    O(1) - key is the first element
        Average case: O(n)
        Worst case:   O(n) - key is last or not present

    Space Complexity:
        O(1) - no additional memory used

    Example:
        >>> linear_search([10, 3, 7, 1, 5], 7)
        2
        >>> linear_search([10, 3, 7, 1, 5], 99)
        -1
    """
    for i in range(len(arr)):
        if arr[i] == key:
            return i
    return -1


def interpolation_search(arr: list[int], key: int) -> int:
    """
    Search for a key in a sorted array using the Interpolation Search algorithm.

    Uses the interpolation formula to estimate the probable position of the key,
    making it faster than binary search for uniformly distributed data.

    Formula:
        pos = low + ((key - arr[low]) * (high - low)) // (arr[high] - arr[low])

    Edge cases handled:
        - Empty array
        - Key out of bounds (less than arr[low] or greater than arr[high])
        - arr[low] == arr[high] to prevent division by zero

    Args:
        arr: A sorted (ascending) list of integers to search through.
        key: The integer value to search for.

    Returns:
        The index of the key if found, or -1 if not found.

    Time Complexity:
        Best case:    O(1)
        Average case: O(log log n) - for uniformly distributed data
        Worst case:   O(n) - for non-uniform distribution

    Space Complexity:
        O(1) - iterative implementation, no extra memory

    Example:
        >>> interpolation_search([1, 3, 5, 7, 9, 11], 7)
        3
        >>> interpolation_search([1, 3, 5, 7, 9, 11], 4)
        -1
    """
    low = 0
    high = len(arr) - 1

    while low <= high and arr[low] <= key <= arr[high]:
        # Prevent division by zero when all elements in range are equal
        if arr[high] == arr[low]:
            if arr[low] == key:
                return low
            return -1

        # Interpolation formula to estimate position
        pos = low + ((key - arr[low]) * (high - low)) // (arr[high] - arr[low])

        if arr[pos] == key:
            return pos
        elif arr[pos] < key:
            low = pos + 1
        else:
            high = pos - 1

    return -1
