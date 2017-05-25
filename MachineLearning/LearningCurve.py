"""
https://github.com/frenky-strasak/My_bachelor_thesis
"""

"""
========================
Plotting Learning Curves
========================

On the left side the learning curve of a naive Bayes classifier is shown for
the digits dataset. Note that the training score and the cross-validation score
are both not very good at the end. However, the shape of the curve can be found
in more complex datasets very often: the training score is very high at the
beginning and decreases and the cross-validation score is very low at the
beginning and increases. On the right side we see the learning curve of an SVM
with RBF kernel. We can see clearly that the training score is still around
the maximum and the validation score could be increased with more training
samples.
"""
# print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.datasets import load_digits
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit
import Get_normalize_data
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier

def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 10)):
    """
    Generate a simple plot of the test and training learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:
          - None, to use the default 3-fold cross-validation,
          - integer, to specify the number of folds.
          - An object to be used as a cross-validation generator.
          - An iterable yielding train/test splits.

        For integer/None inputs, if ``y`` is binary or multiclass,
        :class:`StratifiedKFold` used. If the estimator is not a classifier
        or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validators that can be used here.

    n_jobs : integer, optional
        Number of jobs to run in parallel (default 1).
    """
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt

if __name__ == '__main__':

    final_path = "Final_Experiment\\DividedData\\" + "data_model_1\\"

    X_train, X_test, y_train, y_test = Get_normalize_data.get_all_data(final_path)



    X, y = X_train, y_train


    # SVC is more expensive so we do a lower number of CV iterations:
    cv = ShuffleSplit(n_splits=20 , random_state=0)

    """
    ---------------  SVM  --------------------------
    """
    # title = "Learning Curve ( SVM with rbf kernel )"
    # kernels = ['linear', 'poly', 'rbf']
    # estimator = SVC(kernel=kernels[2], C=110, gamma=0.1)
    """
    --------------- NN ------------------------------
    """
    # title = "Learning Curves (Neural Network alpha=1e-05$)"
    # estimator = MLPClassifier(solver='adam', alpha=1e-05, random_state=1)
    """
    ------------ XGBoost --------------------------
	# max depth = 4, overfitting, 0.96
	# 1. max depth = 1, min_child_weight=1 , gamma=0, 89.5
	# 2. max depth = 3, min_child_weight=5, gamma=0.1, 95.5
	# 3. max_depth = 2, min_child_weight=5, gamma= 0.1 94.5
	"""
    title = "Learning Curves ( XGBoost s)"
    estimator = XGBClassifier(learning_rate=0.1,
                          n_estimators=1000,
                          max_depth=3,
                          min_child_weight=5,
                          gamma=0.1,
                          subsample=0.8,
                          colsample_bytree=0.8,
                          objective='binary:logistic',
                          nthread=4,
                          scale_pos_weight=1,
                          seed=27)
    
    X = np.array(X)
    y = np.array(y)
    """
    ----------------- Random Forest ------------------
    """
    # title = "Learning Curves ( Random forest )"
    # estimator = RandomForestClassifier(n_estimators=500, oob_score='TRUE')


    plot_learning_curve(estimator, title, X, y, cv=cv, n_jobs=10)

    plt.show()
