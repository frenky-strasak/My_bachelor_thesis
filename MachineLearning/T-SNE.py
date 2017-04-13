"""
Take conn_result.txt and create T-SNE.
"""


from time import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import offsetbox
from sklearn import (manifold, datasets)
import Get_normalize_data



path = "c:/Users/frenk/Documents/Skola/Bachelor_thesis/My_bachelor_thesis/MachineLearning/Data_Connection/conn_result.txt"

norm_train_data, train_labels, norm_test_data, test_labels = Get_normalize_data.main(path)



X = norm_train_data + norm_test_data
y = train_labels + test_labels


# Scale and visualize the embedding vectors


def plot_embedding(X, title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure()
    for i in range(len(X)):
        plt.text(X[i, 0], X[i, 1], str(y[i]),
                 color=plt.cm.Set1(y[i] / 6.),
                 fontdict={'weight': 'bold', 'size': 9})

    plt.xticks([]), plt.yticks([])
    if title is not None:
        plt.title(title)

# t-SNE embedding of the digits dataset
print("Computing t-SNE embedding")
tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
t0 = time()
X_tsne = tsne.fit_transform(X)

plot_embedding(X_tsne,
               "t-SNE embedding of the digits (time %.2fs)" %
               (time() - t0))

plt.show()