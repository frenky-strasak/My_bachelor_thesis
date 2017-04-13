from sklearn import svm
import numpy as np


def detect(train_data, train_labels, test_data, test_labels):

    # train_data = np.array(train_data).reshape((1, -1))
    # test_data = np.array(test_data).reshape((1, -1))

    # print train_data

    clf = svm.SVC(gamma=0.001, C=100)
    X,y = train_data, train_labels
    clf.fit(X,y)

    results = (clf.predict(test_data))
    # print "Result more :"
    for i in range(len(test_data)):
        print results[i], " - ", test_labels[i]