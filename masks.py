import math

def mask_0(row, column):
    return (row + column) % 2 == 0

def mask_1(row, column):
    return row % 2 == 0

def mask_2(row, column):
    return column % 3 == 0

def mask_3(row, column):
    return (row + column) % 3 == 0

def mask_4(row, column):
    return (math.floor(row / 2) + math.floor(column / 3)) % 2 == 0

def mask_5(row, column):
    return ((row * column) % 2) + ((row * column) % 3) == 0

def mask_6(row, column):
    return (((row * column) % 2) + ((row * column) % 3)) % 2 == 0

def mask_7(row, column):
    return (((row + column) % 2) + ((row * column) % 3)) % 2 == 0

MASK_FUNCTIONS = {
    0: mask_0,
    1: mask_1,
    2: mask_2,
    3: mask_3,
    4: mask_4,
    5: mask_5,
    6: mask_6,
    7: mask_7
}