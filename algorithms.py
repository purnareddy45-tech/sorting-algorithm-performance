# ============================================
# Sorting Algorithm Performance Comparison
# ============================================

# ---------- Bubble Sort ----------
def bubble_sort(arr):
    comparisons = 0
    swaps = 0

    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            comparisons += 1

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True

        if not swapped:
            break

    return arr, comparisons, swaps


# ---------- Selection Sort ----------
def selection_sort(arr):
    comparisons = 0
    swaps = 0

    n = len(arr)

    for i in range(n):
        min_index = i

        for j in range(i + 1, n):
            comparisons += 1

            if arr[j] < arr[min_index]:
                min_index = j

        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            swaps += 1

    return arr, comparisons, swaps


# ---------- Insertion Sort ----------
def insertion_sort(arr):
    comparisons = 0
    swaps = 0

    n = len(arr)

    for i in range(1, n):
        key = arr[i]
        j = i - 1

        while j >= 0:
            comparisons += 1

            if arr[j] > key:
                arr[j + 1] = arr[j]
                swaps += 1
                j -= 1
            else:
                break

        arr[j + 1] = key

    return arr, comparisons, swaps


# ---------- Merge Sort ----------
def merge_sort(arr):
    comparisons = 0
    swaps = 0

    def merge(left, right):
        nonlocal comparisons

        result = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            comparisons += 1

            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])

        return result

    def divide(array):
        if len(array) <= 1:
            return array

        mid = len(array) // 2

        left = divide(array[:mid])
        right = divide(array[mid:])

        return merge(left, right)

    sorted_array = divide(arr)

    return sorted_array, comparisons, swaps


# ---------- Quick Sort ----------
def quick_sort(arr):
    comparisons = 0
    swaps = 0

    def partition(low, high):
        nonlocal comparisons, swaps

        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            comparisons += 1

            if arr[j] <= pivot:
                i += 1

                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    swaps += 1

        if i + 1 != high:
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            swaps += 1

        return i + 1

    def quick_sort_recursive(low, high):
        if low < high:
            pivot_index = partition(low, high)

            quick_sort_recursive(low, pivot_index - 1)
            quick_sort_recursive(pivot_index + 1, high)

    quick_sort_recursive(0, len(arr) - 1)

    return arr, comparisons, swaps


# ---------- Algorithm Dictionary ----------
SORTING_ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort
}