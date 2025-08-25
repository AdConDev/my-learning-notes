''' Introduction to Algorithms - Chapter 2 - Merge Sort '''


def merge(array, start, middle, end):
    left_len = middle - start + 1
    right_len = end - middle
    left = [0] * (left_len)
    right = [0] * (right_len)
    for index in range(left_len):
        left[index] = array[start + index]
    for index in range(right_len):
        right[index] = array[middle + index + 1]
    l_remain = 0
    r_remain = 0
    fill = start
    while l_remain < left_len and r_remain < right_len:
        if left[l_remain] <= right[r_remain]:
            array[fill] = left[l_remain]
            l_remain = l_remain + 1
        else:
            array[fill] = right[r_remain]
            r_remain = r_remain + 1
        fill = fill + 1
    while l_remain < left_len:
        array[fill] = left[l_remain]
        l_remain = l_remain + 1
        fill = fill + 1
    while r_remain < right_len:
        array[fill] = right[r_remain]
        r_remain = r_remain + 1
        fill = fill + 1


def merge_sort(array, start, end):
    if start >= end:
        return
    middle = (start + end)//2
    merge_sort(array, start, middle)
    merge_sort(array, middle + 1, end)
    merge(array, start, middle, end)


A = [6, 3, 7, 1, 9, 1, 10, 6, 2, 3, 14, 16, 19, 11, 12, 13]
merge_sort(A, 0, len(A) - 1)
print(A)
