import numpy as np
import csv_parser as csv

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
    On prend un mot en entrée est on renvoie son équivalent
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

def get_qr_properties(version, quality):
    capacities = csv.array_to_dict(csv.read('capacities.csv'))

    d = capacities[str(version) + "-" + str(quality)]

    ecPerBlock = d[0]
    group1BlockAmount = d[1]
    group1BlockSize = d[2]
    group2BlockAmount = d[3]
    group2BlockSize = d[4]

    capacity = group1BlockAmount * group1BlockSize + group2BlockAmount * group2BlockSize

    return (capacity, ecPerBlock, (group1BlockAmount, group1BlockSize), (group2BlockAmount, group2BlockSize))


# Tests
# a = np.array([1, 0, 0, 1])
# print(bin(array_to_bin(a)))

#b = 234 << 16 | 237 << 8 | 2
#print(bin_to_array(b))