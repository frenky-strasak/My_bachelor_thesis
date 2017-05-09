import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_gaussian_quantiles
import Get_normalize_data
import DetectionMethods
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn import svm
from xgboost import XGBClassifier

final_path = "Final_Experiment\\DividedData\\" + "data_model_1\\"

X_train, X_test, y_train, y_test = Get_normalize_data.get_all_data(final_path)

"""
 ----------- Learning ------------------
"""

# Create and fit an AdaBoosted decision tree
# bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), #0.910267471959
#                          algorithm="SAMME.R",
#                          n_estimators=500)

bdt = AdaBoostClassifier(RandomForestClassifier(n_estimators=500, oob_score='TRUE')) #0.939603106126


# bdt = AdaBoostClassifier(XGBClassifier())


# kernels = ['linear', 'poly', 'rbf']
# estimator = svm.SVC(kernel=kernels[2], C=110, gamma=0.1)
# bdt = AdaBoostClassifier(estimator, algorithm="SAMME")

bdt.fit(X_train, y_train)

"""
Crossvalidation
"""
DetectionMethods.detect_with_cross_validation(bdt, X_train, y_train)


"""
------------- Testing -------------
"""
DetectionMethods.detect(bdt, X_test, y_test)