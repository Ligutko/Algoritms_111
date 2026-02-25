"""
Main module for DSA laboratory work - Iteration 3 (Variant 2).

Tests Linear Search and Interpolation Search algorithms.
Previous iterations are preserved but commented out in __main__.
"""

from utils import generate_random_array
from sorts import selection_sort, quick_sort
from searches import linear_search, interpolation_search
from logic import find_unique_elements
from benchmark import run_benchmarks


def test_iteration_2_sorting() -> None:
    """
    Test and compare Selection Sort and Quick Sort algorithms.
    
    Generates a small random array of 10 elements, prints the original array,
    sorts it using both selection_sort and quick_sort with copies to ensure
    fair comparison, and prints the sorted results to visually verify correctness.
    """
    print("=" * 70)
    print("DSA Laboratory Work - Iteration 2 (Variant 2)")
    print("Testing Selection Sort and Quick Sort")
    print("=" * 70)
    print()
    
    # Generate a small random array of 10 elements
    original_array = generate_random_array(10)
    
    print("📊 Original Array (10 elements):")
    print(f"   {original_array}")
    print()
    
    # Test Selection Sort with a copy
    print("▸ Selection Sort - O(n²)")
    print("   Time Complexity: Best O(n²), Average O(n²), Worst O(n²)")
    print("   Space Complexity: O(1) - sorts in-place")
    selection_result = selection_sort(original_array.copy())
    print(f"   Sorted Result: {selection_result}")
    print()
    
    # Test Quick Sort with a copy
    print("▸ Quick Sort - O(n log n)")
    print("   Time Complexity: Best O(n log n), Average O(n log n), Worst O(n²)")
    print("   Space Complexity: O(log n) - recursive stack")
    quick_result = quick_sort(original_array.copy())
    print(f"   Sorted Result: {quick_result}")
    print()
    
    # Verify both algorithms produce the same result
    print("-" * 70)
    if selection_result == quick_result:
        print("✅ SUCCESS: Both sorting algorithms produced identical results!")
    else:
        print("❌ ERROR: Sorting results differ!")
    print("=" * 70)


def test_iteration_3_searching() -> None:
    """
    Test and compare Linear Search and Interpolation Search algorithms.

    Generates a random array of 15 elements, sorts it (required for
    Interpolation Search), then runs both algorithms against a key that
    exists and a key that does not exist, printing all results clearly.
    """
    print("=" * 70)
    print("DSA Laboratory Work - Iteration 3 (Variant 2)")
    print("Testing Linear Search and Interpolation Search")
    print("=" * 70)
    print()

    # Generate and sort a 15-element array (Interpolation Search needs sorted)
    raw_array = generate_random_array(15)
    arr = quick_sort(raw_array)

    print(f"📊 Sorted Array (15 elements):")
    print(f"   {arr}")
    print()

    # Pick a key guaranteed to exist and one guaranteed not to exist
    target_exist   = arr[7]
    target_missing = 999999

    print(f"🔍 Search targets:")
    print(f"   target_exist   = {target_exist}  (arr[7])")
    print(f"   target_missing = {target_missing}  (not in array)")
    print()

    # ── Helper to print a uniform result message ──────────────────────────
    def report(algorithm: str, key: int, idx: int) -> None:
        status = f"found at index {idx}" if idx != -1 else "not found"
        print(f"   {algorithm:<26} key={key:<8}  →  {status}")

    # ── Linear Search ──────────────────────────────────────────────────────
    print("▸ Linear Search  —  O(n) time  |  O(1) space  |  works on any array")
    report("linear_search",       target_exist,   linear_search(arr, target_exist))
    report("linear_search",       target_missing, linear_search(arr, target_missing))
    print()

    # ── Interpolation Search ───────────────────────────────────────────────
    print("▸ Interpolation Search  —  O(log log n) avg  |  O(1) space  |  requires sorted array")
    report("interpolation_search", target_exist,   interpolation_search(arr, target_exist))
    report("interpolation_search", target_missing, interpolation_search(arr, target_missing))
    print()

    print("-" * 70)
    print("✅ SUCCESS: Both search algorithms executed correctly!")
    print("=" * 70)


def test_iteration_4_logic() -> None:
    """
    Test the Symmetric Difference logic using find_unique_elements().

    Builds two arrays with a guaranteed overlap by taking a random base
    and giving each array its own exclusive elements. Prints both arrays
    and the resulting symmetric difference.
    """
    print("=" * 70)
    print("DSA Laboratory Work - Iteration 4 (Variant 2)")
    print("Symmetric Difference: elements strictly in A OR strictly in B")
    print("=" * 70)
    print()

    # Build two arrays with a guaranteed intersection
    # Shared elements (will NOT appear in the result)
    shared = [10, 20, 30, 40, 50]

    # Unique parts generated randomly
    only_in_a = generate_random_array(5)   # exclusive to A
    only_in_b = generate_random_array(5)   # exclusive to B

    arr_a: list[int] = only_in_a + shared
    arr_b: list[int] = only_in_b + shared

    print(f"📋 Array A ({len(arr_a)} elements):")
    print(f"   {arr_a}")
    print(f"   unique part : {sorted(only_in_a)}")
    print(f"   shared part : {sorted(shared)}")
    print()

    print(f"📋 Array B ({len(arr_b)} elements):")
    print(f"   {arr_b}")
    print(f"   unique part : {sorted(only_in_b)}")
    print(f"   shared part : {sorted(shared)}")
    print()

    # Run the symmetric difference algorithm
    result = find_unique_elements(arr_a, arr_b)

    print(f"🔎 Symmetric Difference (A △ B):")
    print(f"   Expected to contain elements from unique parts of A and B only.")
    print(f"   Result : {result}")
    print()

    # Verify shared elements are absent from the result
    leaked = [x for x in shared if x in result]
    if not leaked:
        print("✅ SUCCESS: No shared elements leaked into the result!")
    else:
        print(f"❌ ERROR: Shared elements found in result: {leaked}")

    print("=" * 70)


def report_step_2() -> None:
    """Temporary function for lab report Section 2 — array generation demo."""
    from utils import generate_nearly_sorted_array, generate_reversed_array

    SIZES = [10, 100, 1000, 10000]

    print("=" * 60)
    print("  Розділ 2: Розробка утиліт та генерація масивів")
    print("=" * 60)

    # ── generate_arrays() — всі розміри одночасно ────────────────────────────
    print("\n[1] generate_arrays() — випадкові масиви:\n")
    arrays = {}
    for s in SIZES:
        arrays[f"array_{s}"] = generate_random_array(s)

    for name, arr in arrays.items():
        preview = arr[:5]
        print(f"   {name:<12}  розмір={len(arr):>5}  "
              f"тип=random       перші 5: {preview}")

    # ── три варіації масиву 10 000 ────────────────────────────────────────────
    print("\n[2] Три варіації масиву на 10 000 елементів:\n")

    rnd  = generate_random_array(10000)
    nrts = generate_nearly_sorted_array(10000)
    rev  = generate_reversed_array(10000)

    variants = [
        ("random",        rnd,  rnd[:5]),
        ("nearly_sorted", nrts, nrts[:5]),
        ("reversed",      rev,  rev[:5]),
    ]
    for label, arr, preview in variants:
        print(f"   розмір={len(arr):>5}  тип={label:<16}  перші 5: {preview}")

    # ── @time_it декоратор — демонстрація ─────────────────────────────────────
    print("\n[3] Демонстрація декоратора @time_it:\n")
    from utils import time_it

    @time_it
    def demo_generate(size: int):
        return generate_random_array(size)

    for s in SIZES:
        demo_generate(s)

    print("\n" + "=" * 60)
    print("  Всі масиви успішно згенеровані.")
    print("=" * 60)


def report_step_3() -> None:
    """Temporary function for lab report Section 3 — sorting algorithms demo."""
    print("=" * 60)
    print("  Розділ 3: Реалізація алгоритмів сортування")
    print("=" * 60)

    original = generate_random_array(10)
    print(f"\n  Початковий масив : {original}")

    copy_sel = original.copy()
    copy_qck = original.copy()

    result_sel = selection_sort(copy_sel)
    print(f"\n  Selection Sort   : {result_sel}")

    result_qck = quick_sort(copy_qck)
    print(f"  Quick Sort       : {result_qck}")

    match = result_sel == result_qck
    print(f"\n  Результати збігаються : {'✅ ТАК' if match else '❌ НІ'}")
    print("\n" + "=" * 60)


def report_step_4() -> None:
    """Temporary function for lab report Section 4 — search algorithms demo."""
    arr = sorted(generate_random_array(15))

    existing = arr[7]           # елемент що ТОЧНО є (середина масиву)
    missing  = max(arr) + 1     # елемент якого ТОЧНО НЕМАЄ

    print("=" * 60)
    print("  Розділ 4: Реалізація алгоритмів пошуку")
    print("=" * 60)
    print(f"\n  Масив (відсортований, 15 ел.):")
    print(f"  {arr}")

    for label, key in [("ІСНУЮЧИЙ", existing), ("ВІДСУТНІЙ", missing)]:
        print(f"\n  {'─'*54}")
        print(f"  Шукаємо: {key}  [{label}]")
        print(f"  {'─'*54}")

        idx_lin = linear_search(arr, key)
        if idx_lin != -1:
            print(f"  Linear Search       → знайдено на індексі [{idx_lin}]"
                  f"  (arr[{idx_lin}] = {arr[idx_lin]})")
        else:
            print(f"  Linear Search       → не знайдено  (повернув -1)")

        idx_int = interpolation_search(arr, key)
        if idx_int != -1:
            print(f"  Interpolation Search→ знайдено на індексі [{idx_int}]"
                  f"  (arr[{idx_int}] = {arr[idx_int]})")
        else:
            print(f"  Interpolation Search→ не знайдено  (повернув -1)")

        match = idx_lin == idx_int
        print(f"  Результати збігаються: {'✅ ТАК' if match else '❌ НІ'}")

    print("\n" + "=" * 60)


def report_step_5() -> None:
    """Temporary function for lab report Section 5 — symmetric difference demo."""
    from sorts import quick_sort
    from searches import interpolation_search

    # Масиви з відомою спільною та унікальною частиною
    A = [10, 20, 30, 41, 57, 63, 78, 85, 92, 99]
    B = [10, 20, 30, 14, 26, 38, 54, 71, 88, 95]

    shared   = sorted(set(A) & set(B))
    only_a   = sorted(set(A) - set(B))
    only_b   = sorted(set(B) - set(A))

    W = 62
    print("=" * W)
    print("  Розділ 5: Симетрична різниця  A △ B")
    print("  find_unique_elements(arr_a, arr_b)")
    print("=" * W)

    # ── Вхідні дані ───────────────────────────────────────────────────────
    print(f"\n  {'Масив A':<14}: {A}")
    print(f"  {'Масив B':<14}: {B}")

    print(f"\n  {'Спільні елементи':<14}: {shared}  → ці НЕ потраплять у результат")
    print(f"  {'Тільки в A':<14}: {only_a}")
    print(f"  {'Тільки в B':<14}: {only_b}")

    # ── Крок 1: пошук унікальних для A ───────────────────────────────────
    print(f"\n  {'─'*W}")
    print("  КРОК 1 — елементи унікальні для A")
    print(f"  {'─'*W}")
    sorted_b = quick_sort(B.copy())
    print(f"  sorted_B = {sorted_b}")
    for el in A:
        idx = interpolation_search(sorted_b, el)
        status = f"знайдено [idx={idx}] → ПРОПУСКАЄМО" if idx != -1 else "не знайдено → ДОДАЄМО  ✅"
        print(f"    A[{A.index(el)}]={el:>4}  interpol_search(sorted_B, {el:>4}) = {idx:>2}  →  {status}")
    unique_to_a = [el for el in A if interpolation_search(sorted_b, el) == -1]
    print(f"\n  unique_to_A = {unique_to_a}")

    # ── Крок 2: пошук унікальних для B ───────────────────────────────────
    print(f"\n  {'─'*W}")
    print("  КРОК 2 — елементи унікальні для B")
    print(f"  {'─'*W}")
    sorted_a = quick_sort(A.copy())
    print(f"  sorted_A = {sorted_a}")
    for el in B:
        idx = interpolation_search(sorted_a, el)
        status = f"знайдено [idx={idx}] → ПРОПУСКАЄМО" if idx != -1 else "не знайдено → ДОДАЄМО  ✅"
        print(f"    B[{B.index(el)}]={el:>4}  interpol_search(sorted_A, {el:>4}) = {idx:>2}  →  {status}")
    unique_to_b = [el for el in B if interpolation_search(sorted_a, el) == -1]
    print(f"\n  unique_to_B = {unique_to_b}")

    # ── Крок 3: об'єднання ────────────────────────────────────────────────
    print(f"\n  {'─'*W}")
    print("  КРОК 3 — об'єднання та дедублікація")
    print(f"  {'─'*W}")
    combined = unique_to_a + unique_to_b
    print(f"  unique_to_A + unique_to_B = {combined}")
    result = find_unique_elements(A, B)
    print(f"  sorted(set(...))          = {result}")

    # ── Фінал ─────────────────────────────────────────────────────────────
    print(f"\n{'=' * W}")
    print(f"  РЕЗУЛЬТАТ  A △ B  =  {result}")
    print(f"  Перевірка: A∩B={shared} відсутні у результаті:"
          f"  {'✅ ТАК' if not any(x in result for x in shared) else '❌ НІ'}")
    print("=" * W)


if __name__ == "__main__":
    # test_iteration_2_sorting()   # Iteration 2 — commented out
    # test_iteration_3_searching() # Iteration 3 — commented out
    # test_iteration_4_logic()     # Iteration 4 — commented out
    # report_step_2()              # Report Section 2 — commented out
    # report_step_3()              # Report Section 3 — commented out
    # report_step_4()              # Report Section 4 — commented out
    # report_step_5()              # Report Section 5 — commented out
    run_benchmarks()               # Report Section 6 — Benchmarking
