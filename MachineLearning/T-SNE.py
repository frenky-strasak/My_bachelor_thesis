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




"""
------------------ Load train data ----------------------------------
"""
final_path = "Final_Experiment\\DividedData\\" + "features_version_1\\"

X_train, X_test, y_train, y_test = Get_normalize_data.get_all_data(final_path)




print "Malware = 1"
print "Normal = 0"

X = X_train + X_test
y = y_train + y_test

print "amount of data to print:", len(X)

def plot_embedding(draw_test_data, X, title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure()
    my_color =0
    colors = ['black', 'blue', 'red']
    print "embeding, amount:", len(X)
    for i in range(len(X)):
        # draw testing and traing data
        if draw_test_data:
            if i < len(X_train):
                my_color = colors[0]
            else:
                if y[i] == 0:
                    my_color = colors[1]
                else:
                    my_color = colors[2]
        # draw all data
        else:
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
print("Computing T-SNE embedding")
tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
t0 = time()
X_tsne = tsne.fit_transform(X)

# plot all data as 1 and 0
plot_embedding(False, X_tsne,
               "T-SNE - Train data + Test Data") #(time %.2fs)" % (time() - t0))
# plot all data as 1 and 0 with color test data and black train data
plot_embedding(True, X_tsne, "T-SNE Train data + Test Data")

# plot train data
plot_embedding(False, X_tsne[:len(X_train)], "T-SNE Train data")
# plot train data
plot_embedding(False, X_tsne[len(X_train):], "T-SNE Test Data")

Get_normalize_data.write_to_file("X_train.txt", X_tsne[:len(X_train)])
Get_normalize_data.write_to_file("y_train.txt", y[:len(X_train)])

Get_normalize_data.write_to_file("X_test.txt", X_tsne[len(X_train):])
Get_normalize_data.write_to_file("y_test.txt", y[len(X_train):])

plt.show()