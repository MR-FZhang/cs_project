def merge_sort(arr):
    n = len(arr)
    size = 1
    
    while size < n:
        for start in range(0, n, 2 * size):
            mid = start + size - 1
            end = min(start + 2 * size - 1, n - 1)
            merge(arr, start, mid, end)
        size *= 2
    return arr

def merge(arr, start, mid, end):
    left = arr[start:mid+1]
    right = arr[mid+1:end+1]
    i = j = 0
    k = start
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

arr = [2, 5, 4, 6, 6, 4, 6, 5, 7, 9, 3, 7, 8, 15, 5, 2, 8, 5]
print(merge_sort(arr))