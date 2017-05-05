"""
This scripts takes conn4-tuples from "conn_result.txt" and divide them to 3 groups
1. normal data      --
2. malware data     ---      80%
3. test data        -----    20%
"""

import random

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

# def write_to_file(file_name, data_list):
#     index = 0
#     with open("DividedData\\all_features\\" + file_name, 'w') as f:
#         for dataline in data_list:
#             f.write(dataline)
#             index += 1
#     f.close()
#     print file_name,"written lines:", index


def write_to_file(file_name, data_list):
    index = 0
    with open("DividedData\\all_features\\" + file_name, 'w') as f:
        for dataline in data_list:
            f.write(str(dataline) + "\n")
            index += 1
    f.close()
    print file_name,"written lines:", index





"""
Read conn_result.txt
"""
malware_labels = 0
normal_labels = 0

malware_tuples = []
normal_tuples = []
try:
    with open("conn_result.txt") as f:
        for line in f:
            split = line.split('	')
            label = split[29]
            # print label
            if 'MALWARE' in label:
                malware_labels += 1
                malware_tuples.append(line.rstrip())
            if "NORMAL" in label:
                normal_labels += 1
                normal_tuples.append(line.rstrip())
    f.close()
except:
    print "No file."

print "malwares from conn4-tuple:", malware_labels
print "normals from conn4-tuple:", normal_labels



"""
--------------- Divorce conn to normal, malware and test data --------------------
"""

test_data = []
normal_data = []
malware_data = []
"""
take 20% from normal to test
"""
normal_threshold_20_perecent = 1850
# METHOD 1
# random.shuffle(normal_tuples)
test_data += normal_tuples[:1850]
normal_data += normal_tuples[1850:]

# # METHOD 2
# test_normal = 0
# for i in range(len(normal_tuples)):
#     if i%5 == 0:
#         test_data.append(normal_tuples[i])
#         test_normal += 1
#     else:
#         normal_data.append(normal_tuples[i])

# METHOD 3


"""
take 20% from malware to test
"""
malware_threshold_20_perecent = 1626

# METHOD 1
# random.shuffle(malware_tuples)
test_data += malware_tuples[:1626]
malware_data += malware_tuples[1626:]

# METHOD 2
# test_malware = 0
# for i in range(len(malware_tuples)):
#     if i%5 == 0:
#         test_data.append(malware_tuples[i])
#         test_malware += 1
#     else:
#         malware_data.append(malware_tuples[i])

# METHOD 3


"""
---------------------- split each list and normalize ----------------------- 
"""
def getXy(tuples):
    X = []
    y = []
    for line in tuples:
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
    return X,y

normal_X_train, normal_y_train = getXy(normal_data)
malware_X_train, malware_y_train = getXy(malware_data)
X_test, y_test = getXy(test_data)

normal_X_train_n = normalize_data(normal_X_train)
malware_X_train_n = normalize_data(malware_X_train)
X_test_n = normalize_data(X_test)


print "-------------------------------------"
# print "test normal:", test_normal
# print "test malware:", test_malware
print "testdata:", len(test_data)
print "normaldata:", len(normal_data)
print "malwaredata:", len(malware_data)

write_to_file("malware_X_train.txt", malware_X_train_n)
write_to_file("malware_y_train.txt", malware_y_train)

write_to_file("normal_X_train.txt", normal_X_train_n)
write_to_file("normal_y_train.txt", normal_y_train)

write_to_file("X_test.txt", X_test_n)
write_to_file("y_test.txt", y_test)