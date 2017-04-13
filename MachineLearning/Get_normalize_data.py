"""
1. Take data from conn_result.txt
2. normalize this data.
3. call some machine learning algorithm.
"""

import SVM


def get_column(matrix, i):
    return [row[i] for row in matrix]


def set_column(matrix, i):
    for row in range(3):
        matrix[row * 3 + i - 1] = 0


def normalize_data(data):
    for i in range(0, len(data[0])):
        max = 0
        for j in range(len(data)):
            if max < data[j][i]:
                max = data[j][i]
        if max != 0:
            for j in range(len(data)):
                data[j][i] = data[j][i] / float(max)
    return data


def read_res(path):
    train_data = []
    train_labels = []

    test_data = []
    test_labels = []

    # [0] - index
    # [24] - label
    index = 0
    with open(path) as f:
        for line in f:
            split = line.split('	')
            temp = []
            if index < 600:
                for i in range(1, len(split)-1):
                    temp.append(float(split[i]))
                train_data.append(temp)
                if 'MALWARE' in split[24]:
                    train_labels.append(1)
                else:
                    train_labels.append(0)
            else:
                for i in range(1, len(split)-1):
                    temp.append(float(split[i]))
                test_data.append(temp)
                if 'MALWARE' in split[24]:
                    test_labels.append(1)
                else:
                    test_labels.append(0)

            index += 1

    f.close()
    return train_data, train_labels, test_data, test_labels


def main(path):

    train_data, train_labels, test_data, test_labels = read_res(path)
    norm_train_data = normalize_data(train_data)
    norm_test_data = normalize_data(test_data)

    return norm_train_data, train_labels, norm_test_data, test_labels


def read_res2(path):
    malware_data = []

    normal_data = []

    # [0] - index
    # [24] - label
    index = 0
    with open(path) as f:
        for line in f:
            split = line.split('	')
            temp = []
            if 'MALWARE' in split[24]:
                for i in range(1, len(split) - 1):
                    temp.append(float(split[i]))
                malware_data.append(temp)
            if 'NORMAL' in split[24]:
                for i in range(1, len(split) - 1):
                    temp.append(float(split[i]))
                normal_data.append(temp)

            index += 1

    f.close()
    return malware_data, normal_data


def main2(path):
    malware_data, normal_data = read_res2(path)
    norm_malware_data = normalize_data(malware_data)
    norm_normal_data = normalize_data(normal_data)
    return norm_malware_data, norm_normal_data

#
# if __name__ == '__main__':
#     path = "c:/Users/frenk/Documents/Skola/Bachelor_thesis/My_bachelor_thesis/MachineLearning/Data_Connection/conn_result.txt"
#     train_data, train_labels, test_data, test_labels = read_res(path)
#     # print train_data
#     norm_train_data = normalize_data(train_data)
#     norm_test_data = normalize_data(test_data)
#
#     SVM.detect(norm_train_data, train_labels, norm_test_data, test_labels)