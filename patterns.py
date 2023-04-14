import numpy as np
import display

def generate_finder_patterns(version):
    size = (version - 1) * 4 + 21

    topLeft = add_padding(FINDER_PATTERN, 0, size-7, 0, size-7)
    topRight = add_padding(FINDER_PATTERN, size-7, 0, 0, size-7)
    bottomLeft = add_padding(FINDER_PATTERN, 0, size-7, size-7, 0)

    return topLeft + topRight + bottomLeft

def generate_alignment_patterns(version):
    size = (version - 1) * 4 + 21

    P = np.zeros((size, size))
    locations = ALIGNMENT_LOCATIONS[version]

    for x in locations:
        for y in locations:
            if (x - 2 < 7 and (y - 2 < 7 or y + 2 > size - 7)) or (x + 2 > size - 7 and y - 2 < 7):
                continue
            P += add_padding(ALIGNMENT_PATTERN, x - 2, size - x - 3, y - 2, size - y - 3)

    return P

def generate_timing_patterns(version):
    size = (version - 1) * 4 + 21

    P = np.zeros((size, size))

    for x in range(size):
        if x > 7 and x < size - 7 and x % 2 == 0:
            P[6, x] = 1
            P[x, 6] = 1
    
    return P

def generate_dark_module(version):
    size = (version - 1) * 4 + 21

    P = np.zeros((size, size))

    P[4 * version + 9, 8] = 1
    
    return P

def generate_reserved_areas(version):
    size = (version - 1) * 4 + 21

    P = np.zeros((size, size))

    P[:9, :9] = 1
    P[:9, size - 8:size] = 1
    P[size - 8:size, :9] = 1
    P[:, 6] = 1
    P[6, :] = 1

    locations = ALIGNMENT_LOCATIONS[version]

    for x in locations:
        for y in locations:
            if (x - 2 < 7 and (y - 2 < 7 or y + 2 > size - 7)) or (x + 2 > size - 7 and y - 2 < 7):
                continue
            P[x - 2:x + 3, y - 2:y + 3] = 1

    if version > 1:
        P[size - 11:size - 7, :6] = 1
        P[:6, size - 11:size - 7] = 1

    return P

def add_padding(M, l, r, t, b):
    h, w = M.shape

    P = np.zeros((h + t + b, w + l + r))

    for i in range(h):
        for j in range(w):
            P[i+t, j+l] = M[i, j]

    return P

FINDER_PATTERN = np.array([
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1]
])

ALIGNMENT_PATTERN = np.array([
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
])

ALIGNMENT_LOCATIONS = {
    1: [],
    2: [6, 18],
    3: [6, 22],
    4: [6, 26],
    5: [6, 30],
    6: [6, 34],
    7: [6, 22, 38],
    8: [6, 24, 42],
    9: [6, 26, 46],
    10: [6, 28, 50],
    11: [6, 30, 54],
    12: [6, 32, 58],
    13: [6, 34, 62],
    14: [6, 26, 46, 66],
    15: [6, 26, 48, 70],
    16: [6, 26, 50, 74],
    17: [6, 30, 54, 78],
    18: [6, 30, 56, 82],
    19: [6, 30, 58, 86],
    20: [6, 34, 62, 90],
    21: [6, 28, 50, 72, 94],
    22: [6, 26, 50, 74, 98],
    23: [6, 30, 54, 78, 102],
    24: [6, 28, 54, 80, 106],
    25: [6, 32, 58, 84, 110],
    26: [6, 30, 58, 86, 114],
    27: [6, 34, 62, 90, 118],
    28: [6, 26, 50, 74, 98, 122],
    29: [6, 30, 54, 78, 102, 126],
    30: [6, 26, 52, 78, 104, 130],
    31: [6, 30, 56, 82, 108, 134],
    32: [6, 34, 60, 86, 112, 138],
    33: [6, 30, 58, 86, 114, 142],
    34: [6, 34, 62, 90, 118, 146],
    35: [6, 30, 54, 78, 102, 126, 150],
    36: [6, 24, 50, 76, 102, 128, 154],
    37: [6, 28, 54, 80, 106, 132, 158],
    38: [6, 32, 58, 84, 110, 136, 162],
    39: [6, 26, 54, 82, 110, 138, 166],
    40: [6, 30, 58, 86, 114, 142, 170]
}


# Tests
# M = add_padding(FINDER_PATTERN, 3, 4, 2, 5)
# display.show_matrix(M)

# generate_finder_patterns(1)

version = 8
patterns = np.logical_or(np.logical_or(generate_finder_patterns(version),  generate_alignment_patterns(version)), np.logical_or(generate_timing_patterns(version), generate_dark_module(version)))
display.show_matrix(patterns)
display.show_matrix(generate_reserved_areas(version))

