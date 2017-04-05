import os


def find_ssl_log(path, con_uids_dict):
    number_of_ssl = 0
    number_of_x509 = 0

    ssl_malware = 0
    ssl_normal = 0

    x509_malware = 0
    x509_normal = 0

    empty = 0

    normal_d = dict()
    malware_d = dict()
    with open(path + "/bro/ssl.log") as f:
        for line in f:
            if '#' in line:
                continue
            split = line.split('	')

            if 'Background' in con_uids_dict[split[1]] or 'No_Label' in con_uids_dict[split[1]]:
                continue

            if "From-Botnet" in con_uids_dict[split[1]]:
                number_of_ssl += 1
                ssl_malware += 1

            if "From-Normal" in con_uids_dict[split[1]]:
                number_of_ssl += 1
                ssl_normal += 1

            if split[14] == '-':
                empty += 1
                continue


            list_x509 = split[14].split(',')

            if "From-Botnet" in con_uids_dict[split[1]]:
                number_of_x509 += 1
                x509_malware += 1
                try:
                    malware_d[len(list_x509)] += 1
                except:
                    malware_d[len(list_x509)] = 1

            if "From-Normal" in con_uids_dict[split[1]]:
                number_of_x509 += 1
                x509_normal += 1
                try:
                    normal_d[len(list_x509)] += 1
                except:
                    normal_d[len(list_x509)] = 1

    f.close()
    print normal_d
    print malware_d
    print "ssl together:", number_of_ssl
    print "ssl normal:", ssl_normal
    print "ssl malware:", ssl_malware
    print "x509 together:", number_of_x509
    print "x509 normal:", x509_normal
    print "x509 malware:", x509_malware
    print "empty x509 uids in ssl log:", empty
    return number_of_ssl, number_of_x509

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
    # find_ssl_log(path, d)
    return d

if __name__ == '__main__':
    my_path = "c:/Users/frenk/Documents/Skola/Bachelor_thesis/datasets/"

    datasets = os.listdir(my_path)

    number_of_ssl = 0
    number_of_x509 = 0
    for dataset in datasets:
        print "----------" + dataset + "--------------"
        final_path = my_path + dataset
        d = extract_feature(final_path)
        t1, t2 = find_ssl_log(final_path, d)

        number_of_ssl += t1
        number_of_x509 += t2

    print "------together----------"
    print "ssl:", number_of_ssl
    print "x509:", number_of_x509

