''' Introduction to Algorithms - Chapter 2 - Selection Sort '''


def selection_sort(array, length):
    for index in range(0, length - 1):
        key = array[index]
        swap = index + 1
        while swap < length:
            if key > array[swap]:
                key = array[swap]
                array[swap] = array[index]
                array[index] = key
            swap = swap + 1


A = [12, 11, 10, 9, 8, 2, 7, 6, 5, 4, 3, 2, 1]
n = len(A)
selection_sort(A, n)
print(A)