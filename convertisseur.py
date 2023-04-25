# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 09:44:00 2023

@author: Hamza
"""

# première étape d'encodage


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


def conversion_binaire(liste_entiers):
    """
    On prend une liste d'entiers compris entre 0 et 255 et on
    renvoie leur représentation binaire sous forme de liste
    """
    erreur = "Mauvais paramètres données. Il faut une liste d'entier"
    erreur += " compris entre 0 et 255"
    assert type(liste_entiers) == list, erreur
    assert max(liste_entiers) <= 255 and min(liste_entiers) >= 0, erreur
    liste = []
    for entier in liste_entiers:
        binaire = "0"*8
        binaire += bin(entier)[2:]
        liste.append(binaire[-8:])
    return liste


# %% Tests
if __name__ == "__main__":
    # on test la fonction conversion_entier
    assert conversion_entier("A") == [65], "une erreur de test"
    assert conversion_entier("AA") == [65, 65], "une erreur de test"

    assert conversion_binaire([0]) == ["00000000"], "une erreur de test"
    res = ["00000000", "00000001"]
    assert conversion_binaire([0, 1]) == res, "une erreur de test"
