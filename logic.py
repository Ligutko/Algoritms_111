"""
Logic module for DSA laboratory work - Iteration 4 (Variant 2).

Implements the Symmetric Difference task:
Find all elements that exist strictly in array A OR strictly in array B,
but NOT in both (symmetric difference), using our custom sort and search tools.
"""

from sorts import quick_sort
from searches import interpolation_search


def find_unique_elements(arr_a: list[int], arr_b: list[int]) -> list[int]:
    """
    Find elements that exist strictly in array A OR strictly in array B
    (Symmetric Difference), using custom Quick Sort and Interpolation Search.

    Algorithm:
        1. Sort a copy of arr_b with quick_sort.
           Iterate through arr_a — if interpolation_search returns -1,
           the element is unique to A → add to result.
        2. Sort a copy of arr_a with quick_sort.
           Iterate through arr_b — if interpolation_search returns -1,
           the element is unique to B → add to result.
        3. Deduplicate the combined result via set() and return as sorted list.

    Args:
        arr_a: First list of integers.
        arr_b: Second list of integers.

    Returns:
        A sorted list of integers that appear in exactly one of the two arrays
        (symmetric difference).

    Time Complexity:
        O(n log n) for sorting + O(n log log n) for searching ≈ O(n log n)

    Space Complexity:
        O(n) for sorted copies and the result list

    Example:
        >>> find_unique_elements([1, 2, 3, 4], [3, 4, 5, 6])
        [1, 2, 5, 6]
    """
    # ── Step 1: Elements unique to A ──────────────────────────────────────
    sorted_b = quick_sort(arr_b.copy())
    unique_to_a: list[int] = [
        element for element in arr_a
        if interpolation_search(sorted_b, element) == -1
    ]

    # ── Step 2: Elements unique to B ──────────────────────────────────────
    sorted_a = quick_sort(arr_a.copy())
    unique_to_b: list[int] = [
        element for element in arr_b
        if interpolation_search(sorted_a, element) == -1
    ]

    # ── Step 3: Combine and deduplicate ───────────────────────────────────
    result = list(set(unique_to_a + unique_to_b))
    result.sort()
    return result
