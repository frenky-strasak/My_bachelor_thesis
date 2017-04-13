"""
Compute amount of normal and malware ssl flows and amount of normal and malware x509.  
"""

import os


def find_ssl_log(path, con_uids_dict):
    number_of_ssl_M = 0
    number_of_ssl_N = 0
    number_of_x509_M = 0
    number_of_x509_N = 0

    normal_d = dict()
    malware_d = dict()
    with open(path + "/bro/ssl.log") as f:
        for line in f:
            if '#' in line:
                continue
            split = line.split('	')

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
    return number_of_ssl_M, number_of_ssl_N, number_of_x509_M, number_of_x509_N

#14 15 16
def extract_feature(path):
    d = dict()

    with open(path + "/bro/conn_label.log") as f:
        for line in f:
            if '#' in line:
                continue
            split = line.split('	')

            d[split[1]] = split[21]
    f.close()
    return d

if __name__ == '__main__':
    my_path = "c:/Users/frenk/Documents/Skola/Bachelor_thesis/datasets/"

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

        number_of_ssl_M_tot += number_of_ssl_M
        number_of_ssl_N_tot += number_of_ssl_N
        number_of_x509_M_tot += number_of_x509_M
        number_of_x509_N_tot += number_of_x509_N

    print "ssl M:", number_of_ssl_M_tot
    print "ssl N:", number_of_ssl_N_tot
    print "x509 M:", number_of_x509_M_tot
    print "x509 N:", number_of_x509_N_tot
