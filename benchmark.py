"""
Benchmark module for DSA laboratory work - Iteration 5 (Variant 2).

Measures and compares execution times of all sorting and searching algorithms
across multiple array sizes and variations, then prints a formatted summary table.
"""

import time
from utils import (
    generate_arrays,
    generate_random_array,
    generate_nearly_sorted_array,
    generate_reversed_array,
)
from sorts import selection_sort, quick_sort
from searches import linear_search, interpolation_search


# ── Timing helper ─────────────────────────────────────────────────────────────

def _measure(func, *args) -> tuple:
    """
    Measure the wall-clock execution time of func(*args).

    Args:
        func: Callable to benchmark.
        *args: Arguments forwarded to func.

    Returns:
        A tuple (result, elapsed_seconds: float).
    """
    start = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - start
    return result, elapsed


def _fmt_time(seconds: float) -> str:
    """
    Format a duration in seconds into a human-readable string.

    Args:
        seconds: Duration in seconds.

    Returns:
        String like '1.23 ms' or '456.78 µs'.
    """
    if seconds < 1e-3:
        return f"{seconds * 1e6:>8.2f} µs"
    elif seconds < 1:
        return f"{seconds * 1e3:>8.2f} ms"
    return f"{seconds:>8.4f}  s"


# ── Table printer ─────────────────────────────────────────────────────────────

def _print_table(title: str, headers: list[str], rows: list[list[str]]) -> None:
    """
    Print a formatted markdown-style table to the console.

    Args:
        title:   Table heading string.
        headers: List of column header strings.
        rows:    List of rows; each row is a list of cell strings.
    """
    # Compute column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell))

    sep   = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    hdr   = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"

    print()
    print(f"  {title}")
    print(sep)
    print(hdr)
    print(sep)
    for row in rows:
        line = "| " + " | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(headers))) + " |"
        print(line)
    print(sep)


# ── Benchmark runners ──────────────────────────────────────────────────────────

def _bench_sorting() -> None:
    """
    Benchmark Selection Sort and Quick Sort across all array sizes and
    the three 10 000-element variations (random, nearly sorted, reversed).
    """
    arrays = generate_arrays()            # sizes 10, 100, 1000, 10000

    # Extra variations for the largest size
    extra = {
        "10000 (nearly sorted)": generate_nearly_sorted_array(10000),
        "10000 (reversed)":      generate_reversed_array(10000),
    }

    rows: list[list[str]] = []

    for label, arr in list(arrays.items()) + list(extra.items()):
        size_label = label.replace("array_", "")

        _, t_sel  = _measure(selection_sort, arr.copy())
        _, t_qsrt = _measure(quick_sort,     arr.copy())

        rows.append([
            size_label,
            _fmt_time(t_sel).strip(),
            _fmt_time(t_qsrt).strip(),
        ])

    _print_table(
        "SORTING BENCHMARK",
        ["Array variant", "Selection Sort", "Quick Sort"],
        rows,
    )


def _bench_searching() -> None:
    """
    Benchmark Linear Search and Interpolation Search across all array sizes.

    The array is sorted before the interpolation search benchmark to satisfy
    its precondition, but the sorting time is excluded from the measurement.
    """
    arrays = generate_arrays()   # sizes 10, 100, 1000, 10000

    rows: list[list[str]] = []

    for label, arr in arrays.items():
        size_label = label.replace("array_", "")

        # Pick a target guaranteed to exist (middle element of sorted array)
        sorted_arr = quick_sort(arr.copy())
        target = sorted_arr[len(sorted_arr) // 2]

        # Linear search on the unsorted original
        _, t_lin = _measure(linear_search, arr, target)

        # Interpolation search on the pre-sorted array (sort time excluded)
        _, t_ipl = _measure(interpolation_search, sorted_arr, target)

        rows.append([
            size_label,
            str(target),
            _fmt_time(t_lin).strip(),
            _fmt_time(t_ipl).strip(),
        ])

    _print_table(
        "SEARCHING BENCHMARK  (interpolation search runs on pre-sorted array)",
        ["Array size", "Target", "Linear Search", "Interpolation Search"],
        rows,
    )


# ── Public entry point ─────────────────────────────────────────────────────────

def run_benchmarks() -> None:
    """
    Run all sorting and searching benchmarks and print a summary table.

    Covers:
    - Selection Sort vs Quick Sort for sizes 10 / 100 / 1000 / 10000
      and three 10 000-element variations (random, nearly sorted, reversed).
    - Linear Search vs Interpolation Search for sizes 10 / 100 / 1000 / 10000.
    """
    print("=" * 70)
    print("DSA Laboratory Work - Iteration 5 (Variant 2)")
    print("Performance Benchmark Summary")
    print("=" * 70)

    _bench_sorting()
    _bench_searching()

    print()
    print("=" * 70)
    print("✅ Benchmark complete.")
    print("=" * 70)
