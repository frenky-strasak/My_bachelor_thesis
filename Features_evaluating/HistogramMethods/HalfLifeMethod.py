import itertools

def variations_manager():
    dict_sums = dict()

    list_h1 = variace()
    list_h2 = [1]
    list_h3 = [1]

    bigest_sum = -9000000
    smallest_sum = 90000000
    temp_sum = -9000000
    temp_sum_index = 0
    index = 0
    err = 0
    for i in range(0, len(list_h1)):
        for j in range(0, len(list_h2)):
            for k in range(0, len(list_h3)):

                sum = my_function([list_h1[i], list_h2[j], list_h3[k]])

                print str(sum) + " = " + "[ " + str(list_h1[i]) + ", " + str(list_h2[j]) + ", " + str(list_h3[k]) + " ]"

                if bigest_sum < sum:
                    bigest_sum = sum
                if smallest_sum > sum:
                    smallest_sum = sum
                if sum > temp_sum:
                    temp_sum = sum
                    temp_sum_index += 1

                try:
                    if dict_sums[sum]:
                        err += 1
                        dict_sums[sum].append(str(list_h1[i]) + "+" + str(list_h2[j]) + "+" + str(list_h3[k]))
                except:
                    dict_sums[sum] = []
                    dict_sums[sum].append(str(list_h1[i]) + "+" + str(list_h2[j]) + "+" + str(list_h3[k]))

                index += 1

                # print str(sum) + " = " + str(list_h1[i]) + " + " + str(list_h2[j]) + " + " + str(list_h3[k])


    # for key in dict_sums.keys():
    #     if len(dict_sums[key]) > 10:
    #         print "\n", key, "=", dict_sums[key], "\n"

    if temp_sum_index == index:
        print "This function is increasing."
    else:
        print temp_sum_index
        print index

    print ""
    print "number od iterations:", index
    print "Repated:", err
    print "velikost dict:", len(dict_sums)
    print "bigest sum", bigest_sum
    print "smallest sum", smallest_sum


def variace():
    list = []
    for item in itertools.product('0123456789', repeat=2):
        temp = item[0] + item[1]
        # print int(temp)
        list.append(float(temp) + 1)
    return list




def my_function(my_list_temp):
    my_list = list(my_list_temp)
    my_sum = 0

    M = 101
    L = 0
    sorted_list = sorted(my_list)
    m = len(my_list) - 1
    for i in range(len(my_list)):
        # for j in range(len(sorted_list)):
            # if sorted_list[j] == my_list[i]:
            #     try:
            #         L = (sorted_list[j - 1] + sorted_list[j]) / 2
            #     except:
            #         L = (0 + sorted_list[j]) / 2
            #     try:
            #         M = (sorted_list[j + 1] + sorted_list[j]) / 2
            #     except:
            #         M = (2 * sorted_list[j] + sorted_list[j]) / 2

        my_sum += pow(M+L-1, m-i) * (my_list[i] + L -1)

    return my_sum



if __name__ == '__main__':
    res = my_function([50.,1.,100.])
    print res

    # variations_manager()


