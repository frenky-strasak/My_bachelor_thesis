
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
import Get_normalize_data
import DetectionMethods

"""
Read data model 1
"""
final_path = "Final_Experiment\\DividedData\\" + "data_model_1\\"
X_train, X_test, y_train, y_test = Get_normalize_data.get_all_data(final_path)

np_X_train, np_X_test, np_y_train, np_y_test = np.array(X_train), np.array(X_test), np.array(y_train), np.array(y_test)


# Set regularization parameter
for i, C in enumerate((100, 1, 0.01)):
    # turn down tolerance for short training time

    print "i:",i
    clf_l1_LR = LogisticRegression(C=C, penalty='l1', tol=0.01)
    clf_l2_LR = LogisticRegression(C=C, penalty='l2', tol=0.01)
    clf_l1_LR.fit(np_X_train, np_y_train)
    clf_l2_LR.fit(np_X_train, np_y_train)

    coef_l1_LR = clf_l1_LR.coef_.ravel()
    coef_l2_LR = clf_l2_LR.coef_.ravel()

    print clf_l1_LR.score(np_X_test, np_y_test)
    print clf_l2_LR.score(np_X_test, np_y_test)


    # DetectionMethods.detect(coef_l1_LR, np_X_test, np_y_test)
    # DetectionMethods.detect(coef_l2_LR, np_X_test, np_y_test)



