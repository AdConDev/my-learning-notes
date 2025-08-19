''' Introduction to Algorithms - Chapter 2 - Insertion Sort '''


def insertion_sort(array, length):
    for index in range(1, length):
        key = array[index]
        insert = index - 1
        while insert >= 0 and array[insert] > key:
            array[insert + 1] = array[insert]
            insert = insert - 1
        array[insert + 1] = key


def reverse_insertion_sort(array, array_len):
    for index in range(1, array_len):
        key = array[index]
        insert = index - 1
        while insert >= 0 and array[insert] < key:
            array[insert + 1] = array[insert]
            insert = insert - 1
        array[insert + 1] = key


A = [12, 3, 2, 6, 8, 4, 9, 2, 11, 10]
reverse_insertion_sort(A, len(A))
print(A)
insertion_sort(A, len(A))
print(A)
