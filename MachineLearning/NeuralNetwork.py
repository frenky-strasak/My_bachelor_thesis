import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_mldata
from sklearn.neural_network import MLPClassifier
import Get_normalize_data
import DetectionMethods

# mnist = fetch_mldata("MNIST original")
# # rescale the data, use the traditional train/test split
# X, y = mnist.data / 255., mnist.target
# X_train, X_test = X[:60000], X[60000:]
# y_train, y_test = y[:60000], y[60000:]

final_path = "Final_Experiment\\DividedData\\" + "all_features_2\\"


"""
------------------ Load train data ----------------------------------
"""
norm_data_N, labels_N = Get_normalize_data.main2(final_path, "normal_connections.txt")
norm_data_M, labels_M = Get_normalize_data.main2(final_path, "malware_connections.txt")

norm_data = norm_data_N + norm_data_M
labels = labels_N + labels_M

X_train = np.array(norm_data)
y_train = np.array(labels)

"""
--------------- Load test data ----------------------------
"""
norm_test_data, test_labels = Get_normalize_data.main2(final_path, "test_connections.txt")
X_test = np.array(norm_test_data)
y_test = np.array(test_labels)

"""
------------- Algorithm -----------------------
"""

# mlp = MLPClassifier(hidden_layer_sizes=(100,100), max_iter=400, alpha=0.001, #alpha=1e-4,
#                     solver='sgd', verbose=0, tol=1e-4, random_state=1)

mlp = MLPClassifier(hidden_layer_sizes=(50,), max_iter=10, alpha=1e-4,
                    solver='sgd', verbose=0, tol=1e-4, random_state=1,
                    learning_rate_init=.1)


# CrossVaidation
# DetectionMethods.detect_with_cross_validation(mlp, X_train, y_train)



mlp.fit(X_train, y_train)


DetectionMethods.detect(mlp, X_test, y_test)
# print("Training set score: %f" % mlp.score(X_train, y_train))
# print("Test set score: %f" % mlp.score(X_test, y_test))


# fig, axes = plt.subplots(4, 4)
# # use global min / max to ensure all weights are shown on the same scale
# vmin, vmax = mlp.coefs_[0].min(), mlp.coefs_[0].max()
# for coef, ax in zip(mlp.coefs_[0].T, axes.ravel()):
#     ax.matshow(coef.reshape(28, 28), cmap=plt.cm.gray, vmin=.5 * vmin,
#                vmax=.5 * vmax)
#     ax.set_xticks(())
#     ax.set_yticks(())
#
# plt.show()