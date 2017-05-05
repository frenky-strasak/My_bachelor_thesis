"""
python T-SNE.py c:\Users\frenk\Documents\Skola\Bachelor_thesis\My_bachelor_thesis\MachineLearning\Experiment_results\2017_04_20_2127conn\
"""


from time import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import offsetbox
from sklearn import (manifold, datasets)
import Get_normalize_data
import sys


final_path = "Final_Experiment\\DividedData\\" + "all_features_2\\"


"""
------------------ Load train data ----------------------------------
"""
norm_data_N, labels_N = Get_normalize_data.main2(final_path, "normal_connections.txt")
norm_data_M, labels_M = Get_normalize_data.main2(final_path, "malware_connections.txt")

norm_data = norm_data_N + norm_data_M
labels = labels_N + labels_M



"""
--------------- Load test data ----------------------------
"""
norm_test_data, test_labels = Get_normalize_data.main2(final_path, "test_connections.txt")




print "Malware = 1"
print "Normal = 0"

X = norm_data + norm_test_data
y = labels + test_labels

print "amount of data to print:", len(X)

def plot_embedding(X, title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure()
    my_color =0
    colors = ['black', 'blue', 'red']
    print "embeding, amount:", len(X)
    for i in range(len(X)):
        # draw testing and traing data
        # if i < len(norm_data):
        #     my_color = colors[0]
        # else:
        #     if y[i] == 0:
        #         my_color = colors[1]
        #     else:
        #         my_color = colors[2]
        # draw all data
        if y[i] == 0:
            my_color = colors[1]
        else:
            my_color = colors[2]

        plt.text(X[i, 0], X[i, 1], str(y[i]),
                 # color=plt.cm.Set1((1-y[i]) / 6.),
                 color=my_color,
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