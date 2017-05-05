import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_gaussian_quantiles
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

# Create and fit an AdaBoosted decision tree
bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1),
                         algorithm="SAMME.R",
                         n_estimators=500)

bdt.fit(norm_data, labels)

"""
------------- Testing -------------
"""
norm_test_data, test_labels = Get_normalize_data.main2(final_path, "test_connections.txt")
DetectionMethods.detect(bdt, norm_test_data, test_labels)