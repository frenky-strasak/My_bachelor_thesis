"""
https://github.com/frenky-strasak/My_bachelor_thesis
"""

import numpy as np
from sklearn.decomposition import IncrementalPCA
import matplotlib.pyplot as plt
import Get_normalize_data

path = "c:/Users/frenk/Documents/Skola/Bachelor_thesis/My_bachelor_thesis/MachineLearning/Data_Connection/conn_result.txt"

norm_train_data, train_labels, norm_test_data, test_labels = Get_normalize_data.main(path)

data = norm_test_data + norm_test_data
labels = train_labels + test_labels


def plot_embedding(X , title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure()
    for i in range(len(X)):
        plt.text(X[i, 0], X[i, 1], str(labels[i]),
                 color=plt.cm.Set1(labels[i] / 6.),
                 fontdict={'weight': 'bold', 'size': 9})
    plt.xticks([]), plt.yticks([])
    if title is not None:
        plt.title(title)


ipca = IncrementalPCA(n_components=2, batch_size=3)
ipca.fit_transform(norm_train_data)

temp = ipca.transform(data)


plot_embedding(temp, "")
plt.show()










"""
-------------------------------------------------------------------------------------
"""




# import numpy as np
#
# np.random.seed(2342347) # random seed for consistency

# A reader pointed out that Python 2.7 would raise a
# "ValueError: object of too small depth for desired array".
# This can be avoided by choosing a smaller random seed, e.g. 1
# or by completely omitting this line, since I just used the random seed for
# consistency.

# mu_vec1 = np.array([0,0,0])
# cov_mat1 = np.array([[1,0,0],[0,1,0],[0,0,1]])
# class1_sample = np.random.multivariate_normal(mu_vec1, cov_mat1, 20).T
# assert class1_sample.shape == (3,20), "The matrix has not the dimensions 3x20"
#
# mu_vec2 = np.array([1,1,1])
# cov_mat2 = np.array([[1,0,0],[0,1,0],[0,0,1]])
# class2_sample = np.random.multivariate_normal(mu_vec2, cov_mat2, 20).T
# assert class2_sample.shape == (3,20), "The matrix has not the dimensions 3x20"
#
#
#
# print class1_sample





# path = "c:/Users/frenk/Documents/Skola/Bachelor_thesis/My_bachelor_thesis/MachineLearning/Data_Connection/conn_result.txt"
#
# norm_malware_data, norm_normal_data = Get_normalize_data.main2(path)
#
# all_samples_temp = norm_malware_data, norm_normal_data
# all_samples = np.array(all_samples_temp, dtype=float)
#
#
#
#
# # print len(norm_normal_data)
# # print len(norm_malware_data)
# #
# #
# # # 1 -----------------
# # all_samples = np.concatenate((norm_malware_data, norm_normal_data), axis=1)
# # # assert all_samples.shape == (3,40), "The matrix has not the dimensions 3x40"
# #
# from sklearn.decomposition import PCA as sklearnPCA
#
# sklearn_pca = sklearnPCA(n_components=2)
# sklearn_transf = sklearn_pca.fit_transform(all_samples.T)
#
# plt.plot(sklearn_transf[0:346,0],sklearn_transf[0:346,1], 'o', markersize=7, color='blue', alpha=0.5, label='class1')
# plt.plot(sklearn_transf[346:438,0], sklearn_transf[346:438,1], '^', markersize=7, color='red', alpha=0.5, label='class2')
#
# plt.xlabel('x_values')
# plt.ylabel('y_values')
# plt.xlim([-4,4])
# plt.ylim([-4,4])
# plt.legend()
# plt.title('Transformed samples with class labels from matplotlib.mlab.PCA()')
#
# plt.show()
#
#
# # A = [[1,2,3],[4,5,6],[7,8,9]]
# #
# # np_A = np.array(A, dtype=float)
# #
# # print A
# # print np_A