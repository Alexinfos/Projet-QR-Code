import numpy as np
import matplotlib.pyplot as plt

def show_matrix(M, grid=False):
    # Affiche l'image seule
    plt.imshow(M, cmap=plt.get_cmap('binary'))
    plt.show()

# Tests
# M = np.array([
#     [1, 1, 1],
#     [1, 0, 1],
#     [1, 1, 1]
# ])
# show_matrix(M)