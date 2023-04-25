#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 08:59:28 2023

@author: macos
"""

#fc qui code le mot
import polynome_generateur as pg
import division_euclidienne as div
import galois
GF = galois.GF(2**8)


def mot(message, n, k) :
    alpha = GF.primitive_element
    M = []
    for i in range(len(message)):
        M.append(message[i])
        
    g = pg.pol_gen(n,k)
    
    _, R = div.div(M + [0] * (len(g) - 1), g)

    M += R
    
    return M

