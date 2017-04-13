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

    servername_malware = 0
    servername_normal = 0

    x509uids_normal = 0
    x509uids_malware = 0

    index = 0
    with open(path + "/bro/ssl.log") as f:
        for line in f:
            if '#' in line:
                continue
            split = line.split('	')

            # if 'cz.mbank.eu' in split[9]:
            #     print line

            # if split[15] != '(empty)' and split[15] != '-':
            #     print split[15]
            # if '-' in split[14] and not('-' in split[16]):
            #     print line

            if 'Background' in con_uids_dict[split[1]] or 'No_Label' in con_uids_dict[split[1]]:
                continue

            if "From-Botnet" in con_uids_dict[split[1]]:
                if '-' in split[9]:
                    servername_malware += 1
                if '-' in split[14]:
                    x509_malware += 1

            if "From-Normal" in con_uids_dict[split[1]]:
                if '-' in split[9]:
                    servername_normal += 1
                if '-' in split[14]:
                    x509_normal += 1

            # if split[14] == '-':
            #     empty += 1
            #     continue
            #
            # list_x509 = split[14].split(',')
            #
            # print split[15]
            #
            # if "From-Botnet" in con_uids_dict[split[1]]:
            #     number_of_x509 += 1
            #     x509_malware += 1
            #     try:
            #         malware_d[len(list_x509)] += 1
            #     except:
            #         malware_d[len(list_x509)] = 1
            #
            # if "From-Normal" in con_uids_dict[split[1]]:
            #     number_of_x509 += 1
            #     x509_normal += 1
            #     try:
            #         normal_d[len(list_x509)] += 1
            #     except:
            #         normal_d[len(list_x509)] = 1

    f.close()
    # print normal_d
    # print malware_d
    # print "ssl together:", number_of_ssl
    # print "ssl normal:", ssl_normal
    # print "ssl malware:", ssl_malware
    # print "x509 together:", number_of_x509
    # print "x509 normal:", x509_normal
    # print "x509 malware:", x509_malware
    # print "empty x509 uids in ssl log:", empty
    return servername_normal, servername_malware, x509_normal, x509_malware, index


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

    no_server_malware = 0
    no_server_normal = 0
    no_x509_malware = 0
    no_x509_normal = 0
    lines = 0
    for dataset in datasets:
        print "----------" + dataset + "--------------"
        final_path = my_path + dataset

        d = extract_feature(final_path)
        servername_normal, servername_malware, x509_normal, x509_malware, index = find_ssl_log(final_path, d)

        no_server_malware += servername_malware
        no_server_normal += servername_normal
        no_x509_malware += x509_malware
        no_x509_normal += x509_normal
        lines += index

    print "------together----------"
    print "no server name at malware:",no_server_malware
    print "no x509 malware:", no_x509_malware
    print "no server name at normal:", no_server_normal
    print "no x509 normal:", no_x509_normal
    print "number of lines:", lines

