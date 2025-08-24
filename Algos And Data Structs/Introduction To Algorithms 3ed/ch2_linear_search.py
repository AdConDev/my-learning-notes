''' Introduction to Algorithms - Chapter 2 - Linear Search '''


def linear_search(value, array, length):
    found_index = None
    for index in range(0, length):
        if array[index] == value:
            found_index = index
    return found_index


A = [1, 2, 3, 4, 5]
print(linear_search(3, A, 5))
print(linear_search(6, A, 5))
