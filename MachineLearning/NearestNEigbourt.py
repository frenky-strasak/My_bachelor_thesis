import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets
import Get_normalize_data
import DetectionMethods

final_path = "Final_Experiment\\DividedData\\" + "all_features_2\\"

norm_data_N, labels_N = Get_normalize_data.main2(final_path, "normal_connections.txt")
norm_data_M, labels_M = Get_normalize_data.main2(final_path, "malware_connections.txt")

norm_data = norm_data_N + norm_data_M
labels = labels_N + labels_M


"""
 ----------- Learning ------------------
"""

weights = 'distance'
n_neighbors = 15
# we create an instance of Neighbours Classifier and fit the data.
clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
clf.fit(norm_data, labels)


# DetectionMethods.detect_with_cross_validation(clf, norm_data, labels)
"""
------------- Testing -------------
"""
norm_test_data, test_labels = Get_normalize_data.main2(final_path, "test_connections.txt")
DetectionMethods.detect(clf, norm_test_data, test_labels)

X = np.array(norm_data)
y = np.array(labels)
h = .02
"""
------------- Ploting -------------
"""
# Create color maps
# cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
# cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])
# # Plot the decision boundary. For that, we will assign a color to each
# # point in the mesh [x_min, x_max]x[y_min, y_max].
# x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
# y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
# xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
#                      np.arange(y_min, y_max, h))
# Z = clf.predict(xx.ravel(), yy.ravel())
#
# # Put the result into a color plot
# Z = Z.reshape(xx.shape)
# plt.figure()
# plt.pcolormesh(xx, yy, Z, cmap=cmap_light)
#
# # Plot also the training points
# plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold)
# plt.xlim(xx.min(), xx.max())
# plt.ylim(yy.min(), yy.max())
# plt.title("3-Class classification (k = %i, weights = '%s')"
#           % (n_neighbors, weights))
#
# plt.show()