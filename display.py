import numpy as np
import matplotlib.pyplot as plt

def show_matrix(M, palette='binary', showAxis=False):
    # Affiche l'image seule
    plt.imshow(M, cmap=plt.get_cmap(palette))
    if not showAxis:
        plt.axis('off')
    plt.show()

def save_matrix(M, location, palette='binary'):
    plt.imsave(location, M, cmap=plt.get_cmap(palette))

# Tests
# M = np.array([
#     [1, 1, 1],
#     [1, 0, 1],
#     [1, 1, 1]
# ])
# show_matrix(M)