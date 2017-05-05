import Get_normalize_data

"""
Read data model 2
"""
def read_data_model_2():
    model_2_path = "Final_Experiment\\DividedData\\" + "features_parts\\"

    malware_X_train = Get_normalize_data.get_data_from_file(model_2_path, 'malware_X_train.txt')
    malware_y_train = Get_normalize_data.get_labels_from_file(model_2_path, 'malware_y_train.txt')

    normal_X_train = Get_normalize_data.get_data_from_file(model_2_path, 'normal_X_train.txt')
    normal_y_train = Get_normalize_data.get_labels_from_file(model_2_path, 'normal_y_train.txt')

    X_test = Get_normalize_data.get_data_from_file(model_2_path, 'X_test.txt')
    y_test = Get_normalize_data.get_labels_from_file(model_2_path, 'y_test.txt')

    X = malware_X_train + normal_X_train + X_test
    y = malware_y_train + normal_y_train + y_test

    return X, y

"""
Read data model 1
"""
def read_data_model_1():
    final_path = "Final_Experiment\\DividedData\\" + "features_version_1\\"
    X_train, X_test, y_train, y_test = Get_normalize_data.get_all_data(final_path)
    X = X_train + X_test
    y = y_train + y_test

    return X, y

def read_data_model_3():
    final_path = "Final_Experiment\\DividedData\\" + "f_2\\"
    X_train, X_test, y_train, y_test = Get_normalize_data.get_all_data(final_path)
    X = X_train + X_test
    y = y_train + y_test

    return X, y


X_1, y_1 = read_data_model_1()
X_2, y_2 = read_data_model_2()

print "Amouts:"
print len(X_1)
print len(X_2)
print len(y_1)
print len(y_2)

print len(X_1[0])
print len(X_2[0])


dict_1 = dict()
for i in range(len(X_1)):
    key = str(X_1[i])

    try:
        if dict_1[key]:
            print "ERRRRROOOR !!!!"
    except:
        dict_1[key] = y_1[i]


dict_2 = dict()
for i in range(len(X_2)):
    key = str(X_2[i])

    try:
        if dict_2[key]:
            print "ERRRRROOOR !!!!"
    except:
        dict_2[key] = y_2[i]

print "dict:"
print len(dict_1.keys())
print len(dict_2.keys())
#
#
print "Checking dictionaries:"
err = 0
err_2 = 0
index = 0

for key in dict_1.keys():
    try:
        if dict_2[key] == dict_1[key]:
            err += 1
        else:
            print "hovno"
    except:
        err_2 += 1
    index += 1




print "index:", index
print "right:", err
print "bad:", err_2