import itertools
import sys

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

                sum = sebas_function([list_h1[i], list_h2[j], list_h3[k]])

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
    #     if len(dict_sums[key]) > 10:
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


def sebas_function(value_list):
    max_value = max(value_list)
    temp_dict = dict()

    # normalize
    for i in range(len(value_list)):
        value_list[i] = value_list[i] / max_value

    # print value_list

    # round it and add to number
    res_string = ""
    for i in range(len(value_list)):
        value_list[i] = round(10*value_list[i])
        if value_list[i] == 10:
           value_list[i] -= 1
        res_string += str(int(value_list[i]))

    # print res_string

    return int(res_string) #+ 1000000


# Use this !!!
def sebas_function_2(value_list_temp):
    value_list = list(value_list_temp)
    max_value = max(value_list)
    temp_dict = dict()

    # normalize
    for i in range(len(value_list)):
        value_list[i] = value_list[i] / max_value

    # round it and add to main number
    res_string = ""
    for i in range(len(value_list)):
        # return numbers in interval <-0.5, 9.5>
        value_list[i] = (10 * value_list[i]) - 0.5
        # returns numbers: -1,0,1,2,3,4,5,6,7,8,9,10
        value_list[i] = round(value_list[i])
        if value_list[i] == -1.0:
            value_list[i] = 0
        if value_list[i] == 10.0:
           value_list[i] = 9

        res_string += str(int(value_list[i]))

    return int(res_string) #+ 1000000


if __name__ == '__main__':

    my_list = [10000., 100.0, 200.0]

    number = sebas_function_2(my_list)
    print number

    # variations_manager()

