import numpy as np

def array_to_bin(arr):
    binary = 0b0

    for e in arr:
        binary = (binary << 1) | e

    return binary

# Tests
# a = np.array([1, 0, 0, 1])
# print(bin(array_to_bin(a)))