# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 13:37:44 2023

@author: ocean
"""

import convertisseur as con
import galois
GF = galois.GF(2**8)


def mult(a,b):
    """ renvoie le produit des entiers a et b
    utilisation directe du module galois, nous n'avons pas réussi
    à le refaire nous-même"""
    return int(GF(a)*GF(b))


def xor(a,b):
    """ renvoie le XOR (ou exclusif) de deux entiers de GF(256)
    représentés en binaire sous forme de chaine de caractères"""
    assert(len(a)==len(b))
    x = ''
    for i in range(len(a)):
        if a[i]==b[i]:
            x += '0'
        else :
            x += '1'
    return x


def xorpol(A,B):
    """ revoie le XOR (ou exclusif) terme à terme des polynômes A et B
    les deux polynomes sont représentés comme les listes de leurs
    coefficients (entiers de GF(256)) de la plus haute puissance
    à la plus basse
    le résultat est polynome à coefficents entiers dans GF(256)"""
    assert(len(A)==len(B))
    Bb = con.conversion_binaire(B)
    X = []
    for i in range(len(A)):
        x = A[i] ^ B[i]
        X.append(x)

    return X
           

def div(P1,P2):
    """renvoie la division euclidienne du polynome P1 par le
    polynome P2
    les deux polynomes sont représentés comme les listes de leurs
    coefficients (entiers de GF(256)) de la plus haute puissance
    à la plus basse
    P1 et P2 ne sont pas détruits"""
    Q = []
    R = P1.copy()
    deg = len(P1) - len(P2)
    for i in range(deg, -1, -1):
        tmp = P2.copy()
        for j in range(len(tmp)):
            tmp[j] = mult(tmp[j], R[0])
        for j in range(i):
            tmp.append(0)
        Q.append(R[0])
        R = xorpol(R,tmp)[1:]
        
    return Q, R
