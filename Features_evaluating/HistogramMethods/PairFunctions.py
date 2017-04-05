import itertools
import math

prime_arr = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]


def prime_number_function():

    dict_sums = dict()

    list_h1 = variace()
    list_h2 = variace()
    list_h3 = variace()

    bigest_sum = 0
    index = 0
    err = 0
    for i in range(0, len(list_h1)):
        for j in range(0, len(list_h2)):
            for k in range(0, len(list_h3)):
                # sum = math.pow(list_h1[i], 2) + math.pow(list_h2[j], 3) + math.pow(list_h3[k], 5)
                sum = cantor([list_h1[i], list_h2[j], list_h3[k]])

                if bigest_sum < sum:
                    bigest_sum = sum

                try:
                    if dict_sums[sum]:
                        # print "Error:", sum, list_h1[i], list_h2[j], list_h3[k]
                        err += 1
                        dict_sums[sum].append(str(list_h1[i]) + "+" + str(list_h2[j]) + "+" + str(list_h3[k]))
                except:
                    dict_sums[sum] = []
                    dict_sums[sum].append(str(list_h1[i]) + "+" + str(list_h2[j]) + "+" + str(list_h3[k]))

                index += 1

    print index, err
    print "velikost dict:", len(dict_sums)
    print bigest_sum

    for key in dict_sums.keys():
        if len(dict_sums[key]) > 1:
            print "\n", key, "=", dict_sums[key], "\n"


def sebas_function(value_list):
    max_value = max(value_list)
    temp_dict = dict()
    # normalize
    for i in range(len(value_list)):
        value_list[i] = value_list[i] / max_value

    print value_list
    temp_list = sorted(value_list)

    for i in range(len(temp_list)):
        temp_dict[temp_list[i]] = (i+1)

    for i in range(len(value_list)):
        value_list[i] = temp_dict[value_list[i]]

    print value_list


def variace():
    list = []
    for item in itertools.product('0123456789', repeat=2):
        temp = item[0] + item[1]
        # print int(temp)
        list.append(float(temp) + 1)
    return list



"""
 ------------------------- Cantor pair function ------------------------------
"""
def cantor(list):
    norm_list, max_value, sum_list = normalize(list)
    cantor_res = cantor_manager(norm_list)
    result = cantor_res * sum_list
    return result

    # without normalize
    # cantor_res = cantor_manager(list)
    # result = cantor_res
    # return result

def normalize(list):
    max_value = max(list)
    sum_list = 0
    for i in range(len(list)):
        sum_list += list[i]
        list[i] = list[i] / max_value
    return list, max_value, sum_list


def cantor_manager(list):
    sum = 0
    if len(list) < 2:
        print "Error: List has few elements."

    for i in range(len(list)):
        if i == 1:
            sum = cantor_pairing_function([list[0], list[1]])
        if i >1:
            sum = cantor_pairing_function([sum, list[i]])

    return sum


def cantor_pairing_function(list):
    x = list[0]
    y = list[1]

    sum = 0.5*((x+y+1)*(x+y)) + y

    return sum


"""
----------------- next function ------------------
"""


def my_function(list):
    sum = 0

    M = 0
    L = 0
    sorted_list = sorted(list)
    for i in range(len(list)):
        for j in range(len(sorted_list)):
            if sorted_list[j] == list[i]:
                try:
                    L = (list[i-1] + list[i]) / 2
                except:
                    L = (0 + list[i]) / 2
                try:
                    M = (list[i+1] + list[i]) / 2
                except:
                    M = (2*list[i] + list[i]) / 2

        sum += pow(M+L-1, )


if __name__ == '__main__':
    # it generates variations
    prime_number_function()

    # sebas function
    # sebas_function([2.0, 50.0, 43.0, 80.0, 5000.0, 0.0, 23.0, 1564.0])

    # just cantor algorithm
    # list = [11.0, 10.0, 3000.0, 456.0, 1000000.0]
    # print cantor(list)


