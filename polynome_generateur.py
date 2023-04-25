# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 14:43:07 2023

@author: ocean
"""

import galois
import convertisseur as con
GF = galois.GF(2**8)


def pol_gen(n,k):
    """ renvoie le polynome generateur du code (n,k) en décimal
    le polynome sera représenté par la liste de ses coefficients,
    de la pluissance la plus haute à la puissance la plus basse"""
    alpha = GF.primitive_element
    #on initialise les racines
    pol=[1]
    for i in range(n-k):
        pol = prod(pol,[1,alpha**i])
    return pol


def xor(a,b):
    """ renvoie le XOR (ou exclusif) de deux entiers de GF(256)
    le résultat est un entier de GF(256)"""
    A = con.conversion_binaire([a])[0]
    B = con.conversion_binaire([b])[0]
    assert(len(A) == len(B))
    X = ''
    for i in range(len(A)):
        if A[i] == B[i] :
            X += '0'
        else :
            X += '1'
    x = int(X, 2)
    return x


def mult(a,b):
    """ renvoie le produit des entiers a et b
    utilisation directe du module galois, nous n'avons pas réussi
    à le refaire nous-même"""
    return int(GF(a)*GF(b))


def prod(P1,P2):
    """ renvoie le produit de P1 et P2, où P2 est de degré 1
    P1 et P2 sont preprésentés en puissances de alpha"""
    assert(len(P2)==2)
    n = len(P1) - 1
    if n == -1 : 
        return [] #polynome nul
    
    P = [mult(P2[0],P1[0])]
    for i in range(n):
        M1 = mult(P2[1],P1[i])
        M2 = mult(P2[0],P1[i+1])
        X = xor(M1,M2)
        P.append(X)
    P.append(mult(P1[-1],P2[1]))
    return P


