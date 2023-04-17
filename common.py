import numpy as np

def array_to_bin(arr):
    binary = 0b0

    for e in arr:
        binary = (binary << 1) | e

    return binary

def bytearray_to_bin(arr):
    binary = 0b0

    for e in arr:
        binary = (binary << 8) | e

    return binary

def bin_to_array(binData):
    dataArray = []

    while binData != 0b0:
        dataArray.append(binData & 0b11111111)
        binData = binData >> 8

    return dataArray

def conversion_entier(mot):
    """
    On prend un mot en entré est on renvoie son équivalent
    binaire qu'on écrira comme une liste d'entiers pour
    gagner en lisibilité

    exemple :
        00000000 = 0
        00000001 = 1
        ...
        11111111 = 255
    """
    erreur = "Il faut donner une chaine de caractère en paramètre"
    assert type(mot) == str, erreur
    liste = []
    for lettre in mot:
        liste.append(ord(lettre))
    return liste

BIN_CAPACITIES = {
    '1L': 17,
    '1M': 14,
    '1Q': 11,
    '1H': 7,
    '2L': 32,
    '2M': 26,
    '2Q': 20,
    '2H': 14,
    '3L': 53,
    '3M': 42,
    '3Q': 32,
    '3H': 24,
    '4L': 78,
    '4M': 62,
    '4Q': 46,
    '4H': 34,
    '5L': 106,
    '5M': 84,
    '5Q': 60,
    '5H': 44,
    '6L': 134,
    '6M': 106,
    '6Q': 74,
    '6H': 58,
    '7L': 154,
    '7M': 122,
    '7Q': 86,
    '7H': 64,
    '8L': 192,
    '8M': 152,
    '8Q': 108,
    '8H': 84,
    '9L': 230,
    '9M': 180,
    '9Q': 130,
    '9H': 98,
    '10L': 271,
    '10M': 213,
    '10Q': 151,
    '10H': 119,
    '11L': 321,
    '11M': 251,
    '11Q': 177,
    '11H': 137,
    '12L': 367,
    '12M': 287,
    '12Q': 203,
    '12H': 155,
    '13L': 425,
    '13M': 331,
    '13Q': 241,
    '13H': 177,
    '14L': 458,
    '14M': 362,
    '14Q': 258,
    '14H': 194,
    '15L': 520,
    '15M': 412,
    '15Q': 292,
    '15H': 220,
    '16L': 586,
    '16M': 450,
    '16Q': 322,
    '16H': 250,
    '17L': 644,
    '17M': 504,
    '17Q': 364,
    '17H': 280,
    '18L': 718,
    '18M': 560,
    '18Q': 394,
    '18H': 310,
    '19L': 792,
    '19M': 624,
    '19Q': 442,
    '19H': 338,
    '20L': 858,
    '20M': 666,
    '20Q': 482,
    '20H': 382,
    '21L': 929,
    '21M': 711,
    '21Q': 509,
    '21H': 403,
    '22L': 1003,
    '22M': 779,
    '22Q': 565,
    '22H': 439,
    '23L': 1091,
    '23M': 857,
    '23Q': 611,
    '23H': 461,
    '24L': 1171,
    '24M': 911,
    '24Q': 661,
    '24H': 511,
    '25L': 1273,
    '25M': 997,
    '25Q': 715,
    '25H': 535,
    '26L': 1367,
    '26M': 1059,
    '26Q': 751,
    '26H': 593,
    '27L': 1465,
    '27M': 1125,
    '27Q': 805,
    '27H': 625,
    '28L': 1528,
    '28M': 1190,
    '28Q': 868,
    '28H': 658,
    '29L': 1628,
    '29M': 1264,
    '29Q': 908,
    '29H': 698,
    '30L': 1732,
    '30M': 1370,
    '30Q': 982,
    '30H': 742,
    '31L': 1840,
    '31M': 1452,
    '31Q': 1030,
    '31H': 790,
    '32L': 1952,
    '32M': 1538,
    '32Q': 1112,
    '32H': 842,
    '33L': 2068,
    '33M': 1628,
    '33Q': 1168,
    '33H': 898,
    '34L': 2188,
    '34M': 1722,
    '34Q': 1228,
    '34H': 958,
    '35L': 2303,
    '35M': 1809,
    '35Q': 1283,
    '35H': 983,
    '36L': 2431,
    '36M': 1911,
    '36Q': 1351,
    '36H': 1051,
    '37L': 2563,
    '37M': 1989,
    '37Q': 1423,
    '37H': 1093,
    '38L': 2699,
    '38M': 2099,
    '38Q': 1499,
    '38H': 1139,
    '39L': 2809,
    '39M': 2213,
    '39Q': 1579,
    '39H': 1219,
    '40L': 2953,
    '40M': 2331,
    '40Q': 1663,
    '40H': 1273
}

# Tests
# a = np.array([1, 0, 0, 1])
# print(bin(array_to_bin(a)))

b = 234 << 16 | 237 << 8 | 2
print(bin_to_array(b))