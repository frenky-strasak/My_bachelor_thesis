"""
Compute amount of normal and malware ssl flows and amount of normal and malware x509.  
"""

import os
import sys

def read_x509(path):
    index = 0
    try:
        with open(path + "/bro/x509.log") as f:
            for line in f:
                if '#' == line[0]:
                    # print line
                    continue
                index += 1
        f.close()
    except:
        print "Error: no x509 file."
    print "Number of lines in x509.log:", index

def find_ssl_log(path, con_uids_dict):
    number_of_ssl_M = 0
    number_of_ssl_N = 0
    number_of_x509_M = 0
    number_of_x509_N = 0

    ssl_dict = dict()
    index = 0
    normal_d = dict()
    malware_d = dict()
    with open(path + "/bro/ssl.log") as f:
        for line in f:
            if '#' == line[0]:
                # print line
                continue

            index += 1
            split = line.split('	')
            ssl_uid = split[1]
            try:
                if ssl_dict[ssl_uid]:
                    continue
            except:
                ssl_dict[ssl_uid] = 1



            if "Background" in con_uids_dict[split[1]]:
                continue

            if "From-Botnet" in con_uids_dict[split[1]]:
                number_of_ssl_M += 1

            if "From-Normal" in con_uids_dict[split[1]]:
                number_of_ssl_N += 1

            if split[14] == '-':
                continue

            list_x509 = split[14].split(',')

            if "From-Botnet" in con_uids_dict[split[1]]:
                number_of_x509_M += 1
                # try:
                #     malware_d[len(list_x509)] += 1
                # except:
                #     malware_d[len(list_x509)] = 1

            if "From-Normal" in con_uids_dict[split[1]]:
                number_of_x509_N += 1
                # try:
                #     normal_d[len(list_x509)] += 1
                # except:
                #     normal_d[len(list_x509)] = 1

    f.close()
    print "Malware flows in ssl.log:", number_of_ssl_M
    print "Normal flows in ssl.log:", number_of_ssl_N
    print "Number of lines in ssl.log:", index
    print "Malware certificates(lines) in x509 from ssl.log:", number_of_x509_M
    print "Normal certificates(lines) in x509 from ssl.log:", number_of_x509_N
    return number_of_ssl_M, number_of_ssl_N, number_of_x509_M, number_of_x509_N

#14 15 16
def extract_feature(path):
    d = dict()
    normal = 0
    malware = 0
    index = 0
    with open(path + "/bro/conn_label.log") as f:
        for line in f:
            if '#' == line[0]:
                continue
            split = line.split('	')

            try:
                if d[split[1]]:
                    print "Error: more uids in conn.log!!!!!!!11"
            except:
                d[split[1]] = split[21]

            if "From-Botnet" in split[21]:
                malware += 1
            if "From-Normal" in split[21]:
                normal += 1
            index += 1
    f.close()

    print "Malware flows in conn.log:", malware
    print "Normal flows in conn.log:", normal
    print "Number of lines in conn.log:", index
    return d


if __name__ == '__main__':

    if len(sys.argv) > 1:
        my_path = sys.argv[1]
    else:
        my_path = None
    # my_path = "C:/Users/frenk/Desktop/dataset_test/"

    datasets = os.listdir(my_path)

    number_of_ssl_M_tot = 0
    number_of_ssl_N_tot = 0
    number_of_x509_M_tot = 0
    number_of_x509_N_tot = 0
    for dataset in datasets:
        print "----------" + dataset + "--------------"
        final_path = my_path + dataset
        d = extract_feature(final_path)
        number_of_ssl_M, number_of_ssl_N, number_of_x509_M, number_of_x509_N = find_ssl_log(final_path, d)
        read_x509(final_path)

        number_of_ssl_M_tot += number_of_ssl_M
        number_of_ssl_N_tot += number_of_ssl_N
        number_of_x509_M_tot += number_of_x509_M
        number_of_x509_N_tot += number_of_x509_N

    print "-----------------------------------------------------"
    print "---------- Results for all experiments --------------"
    print "-----------------------------------------------------"
    print "Total malware flow from ssl.logs:", number_of_ssl_M_tot
    print "Total normal flow from ssl.logs:", number_of_ssl_N_tot
    print "Total malware certificate in x509.logs:", number_of_x509_M_tot
    print "Total normal certificate in x509.logs:", number_of_x509_N_tot
