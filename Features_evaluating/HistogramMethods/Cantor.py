import math
import itertools


def variations_manager():
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

                sum = cantor([list_h1[i], list_h2[j], list_h3[k]])

                if bigest_sum < sum:
                    bigest_sum = sum

                try:
                    if dict_sums[sum]:
                        err += 1
                        dict_sums[sum].append(str(list_h1[i]) + "+" + str(list_h2[j]) + "+" + str(list_h3[k]))
                except:
                    dict_sums[sum] = []
                    dict_sums[sum].append(str(list_h1[i]) + "+" + str(list_h2[j]) + "+" + str(list_h3[k]))

                index += 1

    # for key in dict_sums.keys():
    #     if len(dict_sums[key]) > 2:
    #         print "\n", key, "=", dict_sums[key], "\n"

    print ""
    print index, err
    print "velikost dict:", len(dict_sums)
    print "bigest sum", bigest_sum


def variace():
    list = []
    for item in itertools.product('0123456789', repeat=2):
        temp = item[0] + item[1]
        # print int(temp)
        list.append(float(temp) + 1)
    return list


def cantor(list):
    # norm_list, max_value, sum_list = normalize(list)
    # cantor_res = cantor_manager(list)
    # result = cantor_res * sum_list
    # return result

    # without normalize
    cantor_res = cantor_manager(list)
    result = cantor_res
    return result


def normalize(old_list):
    max_value = max(old_list)
    sum_list = 0
    temp_list = list(old_list)
    for i in range(len(temp_list)):
        sum_list += temp_list[i]
        temp_list[i] = temp_list[i] / max_value
    return temp_list, max_value, sum_list


def cantor_manager(list):
    sum = 0
    if len(list) < 2:
        print "Error: List has few elements."

    for i in range(len(list)):
        if i == 1:
            sum = cantor_pairing_function([list[0], list[1]])
        if i > 1:
            sum = cantor_pairing_function([sum, list[i]])

    return sum


def cantor_pairing_function(list):
    x = list[0]
    y = list[1]

    sum = 0.5*((x+y+1)*(x+y)) + y

    return sum




if __name__ == '__main__':
    # easy way to try
    # list = [1000000,1000000,10000000]
    # print cantor(list)

    # try variations
    variations_manager()
    
