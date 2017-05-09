"""
Divide data from conn_result.txt to payload data (without conn_tuple) and save again 
"""
from sklearn.model_selection import train_test_split


def normalize_data(data):
    for i in range(0, len(data[0])):
        max = 0
        for j in range(len(data)):
            if max < data[j][i]:
                max = data[j][i]
        if max != 0:
            for j in range(len(data)):
                if data[j][i] != -1:
                    data[j][i] = data[j][i] / float(max)
    return data


def write_to_file(file_name, data_list):
    index = 0
    with open("DividedData\\data_model_1\\" + file_name, 'w') as f:
        for dataline in data_list:
            f.write(str(dataline) + "\n")
            index += 1
    f.close()
    print file_name,"written lines:", index


def write_to_file_2(file_name, data_list):
    index = 0
    with open("DividedData\\features_parts\\" + file_name, 'w') as f:
        for dataline in data_list:
            f.write(str(dataline) + "\n")
            index += 1
    f.close()
    print file_name,"written lines:", index



all_tuples = []


try:
    with open("conn_result.txt") as f:
    # with open("DividedData\\all_features_2\\malware_connections.txt") as f:
        for line in f:
            all_tuples.append(line)
    f.close()
except:
    print "No file."


X = []
y = []
for line in all_tuples:
    split = line.split('	')
    label = split[29]
    number_label = -1

    if 'MALWARE' in label:
        number_label = 1
    if "NORMAL" in label:
        number_label = 0
    if number_label == -1:
        print "ERROR: label is -1."
        break

    temp = []
    for i in range(1, 29):
        temp.append(float(split[i]))
    X.append(temp)
    y.append(number_label)


# normalize X
norm_X = normalize_data(X)
print "velikost naseho krasneho celeho X je:", len(X)

# split data by sklearn library
X_train, X_test, y_train, y_test = train_test_split(norm_X, y, test_size=.2, random_state=35)

# Write train data
write_to_file('X_train.txt', X_train)
write_to_file('y_train.txt', y_train)

# Write test data
write_to_file('X_test.txt', X_test)
write_to_file('y_test.txt', y_test)

"""
Create part data model
"""
# normal_data = []
# normal_labels = []
# malware_data = []
# malware_labels = []
# test_data = []
# test_labels = []
# for i in range(len(X)):
#     if i%5 == 0:
#         test_data.append(X[i])
#         test_labels.append(y[i])
#     else:
#         if y[i] == 0:
#             normal_data.append(X[i])
#             normal_labels.append(y[i])
#         if y[i] == 1:
#             malware_data.append(X[i])
#             malware_labels.append(y[i])

# write_to_file_2('malware_X_train.txt', malware_data)
# write_to_file_2('malware_y_train.txt', malware_labels)
#
# write_to_file_2('normal_X_train.txt', normal_data)
# write_to_file_2('normal_y_train.txt', normal_labels)
#
# write_to_file_2('X_test.txt', test_data)
# write_to_file_2('y_test.txt', test_labels)




