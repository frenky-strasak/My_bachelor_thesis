"""
Compute amount of normal and malware ssl flows and amount of normal and malware x509.  
"""

import os
import sys

def read_x509(path):
    x509_dict = dict()
    index = 0
    try:
        with open(path + "/bro/x509.log") as f:
            for line in f:
                if '#' == line[0]:
                    continue
                split = line.split('	')
                try:
                    if x509_dict[split[1]] != 1:
                        print "Error !!!! more x509"
                except:
                    x509_dict[split[1]] = line
                index += 1
        f.close()
    except:
        print "Error: no x509 file."
    print "Number of lines in x509.log:", index
    return x509_dict

def find_ssl_log(path, con_uids_dict, normal_cer_dict, malware_cer_dict, normal_conn_tuples_dict, malware_conn_tuples_dict):
    number_of_ssl_M = 0
    number_of_ssl_N = 0
    number_of_x509_M = 0
    number_of_x509_N = 0

    ssl_dict = dict()
    index = 0
    normal_d = dict()
    malware_d = dict()

    x509_dict = read_x509(final_path)
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

            conn_split = con_uids_dict[split[1]].split('	')
            onnection_index = conn_split[2], conn_split[4], conn_split[5], conn_split[6]
            label = conn_split[21]
            if "Background" in label:
                continue

            if "From-Botnet" in label:
                number_of_ssl_M += 1
                try:
                    malware_conn_tuples_dict[onnection_index] += 1
                except:
                    malware_conn_tuples_dict[onnection_index] = 1

            if "From-Normal" in label:
                number_of_ssl_N += 1
                try:
                    normal_conn_tuples_dict[onnection_index] += 1
                except:
                    normal_conn_tuples_dict[onnection_index] = 1

            if split[14] == '-' or '(object)' == split[14]:
                continue

            list_x509 = split[14].split(',')
            x509_key = list_x509[0]



            x509_line = x509_dict[x509_key]
            x509_split = x509_line.split('	')

            cert_serial = x509_split[3]
            if "From-Botnet" in label:
                number_of_x509_M += 1
                try:
                    malware_cer_dict[cert_serial] += 1
                except:
                    malware_cer_dict[cert_serial] = 1

            if "From-Normal" in label:
                number_of_x509_N += 1
                try:
                    normal_cer_dict[cert_serial] += 1
                except:
                    normal_cer_dict[cert_serial] = 1

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
                    print "Error: more uids in conn.log!!!!!!!"
            except:
                d[split[1]] = line

            if "From-Botnet" in split[21]:
                malware += 1
            if "From-Normal" in split[21]:
                normal += 1
            index += 1
    f.close()

    print "Malware flows in conn.log:", malware
    print "Normal flows in conn.log:", normal
    print "Number of lines in conn.log:", index
    return normal, malware, d


if __name__ == '__main__':

    if len(sys.argv) > 1:
        my_path = sys.argv[1]
    else:
        my_path = None
    # my_path = "C:/Users/frenk/Desktop/dataset_test/"

    # datasets = os.listdir(my_path)

    datasets = [
        "CTU-Malware-Capture-Botnet-1",
        "CTU-Malware-Capture-Botnet-102",
        "CTU-Malware-Capture-Botnet-110-1",
        "CTU-Malware-Capture-Botnet-110-2",
        "CTU-Malware-Capture-Botnet-111-1",
        "CTU-Malware-Capture-Botnet-111-5",
        "CTU-Malware-Capture-Botnet-112-1",
        "CTU-Malware-Capture-Botnet-112-2",
        "CTU-Malware-Capture-Botnet-112-4",
        "CTU-Malware-Capture-Botnet-116-1",
        "CTU-Malware-Capture-Botnet-116-2",
        "CTU-Malware-Capture-Botnet-116-4",
        "CTU-Malware-Capture-Botnet-120-1",
        "CTU-Malware-Capture-Botnet-123-1",
        "CTU-Malware-Capture-Botnet-129-1",
        "CTU-Malware-Capture-Botnet-137-1",
        "CTU-Malware-Capture-Botnet-138-1",
        "CTU-Malware-Capture-Botnet-140-1",
        "CTU-Malware-Capture-Botnet-140-2",
        "CTU-Malware-Capture-Botnet-141-1",
        "CTU-Malware-Capture-Botnet-141-2",
        "CTU-Malware-Capture-Botnet-142-1",
        "CTU-Malware-Capture-Botnet-143-1",
        "CTU-Malware-Capture-Botnet-144-1",
        "CTU-Malware-Capture-Botnet-145-1",
        "CTU-Malware-Capture-Botnet-153-1",
        "CTU-Malware-Capture-Botnet-157-1",
        "CTU-Malware-Capture-Botnet-162-1",
        "CTU-Malware-Capture-Botnet-162-2",
        "CTU-Malware-Capture-Botnet-163-1",
        "CTU-Malware-Capture-Botnet-164-1",
        "CTU-Malware-Capture-Botnet-169-3",
        "CTU-Malware-Capture-Botnet-17-1",
        "CTU-Malware-Capture-Botnet-17-2",
        "CTU-Malware-Capture-Botnet-188-2",
        "CTU-Malware-Capture-Botnet-188-4",
        "CTU-Malware-Capture-Botnet-208-2",
        "CTU-Malware-Capture-Botnet-219-2",
        "CTU-Malware-Capture-Botnet-25-1",
        "CTU-Malware-Capture-Botnet-25-2",
        "CTU-Malware-Capture-Botnet-25-3",
        "CTU-Malware-Capture-Botnet-25-4",
        "CTU-Malware-Capture-Botnet-25-5",
        "CTU-Malware-Capture-Botnet-25-6",
        "CTU-Malware-Capture-Botnet-27-1",
        "CTU-Malware-Capture-Botnet-27-2",
        "CTU-Malware-Capture-Botnet-31-1",
        "CTU-Malware-Capture-Botnet-35-1",
        "CTU-Malware-Capture-Botnet-61-1",
        "CTU-Malware-Capture-Botnet-69",
        "CTU-Malware-Capture-Botnet-78-1",
        "CTU-Malware-Capture-Botnet-78-2",
        "CTU-Malware-Capture-Botnet-90",
        "CTU-Normal-12",
        "CTU-Normal-6-filtered",
        "CTU-Normal-7",
        "CTU-Normal-8-1",
        "CTU-Normal-8-2",
        "CTU-Normal-9"
    ]

    number_of_conn_M = 0
    number_of_conn_N = 0
    number_of_ssl_M_tot = 0
    number_of_ssl_N_tot = 0
    number_of_x509_M_tot = 0
    number_of_x509_N_tot = 0
    malware_cer_dict = dict()
    normal_cer_dict = dict()
    malware_conn_tuples_dict = dict()
    normal_conn_tuples_dict = dict()
    for dataset in datasets:
        print "----------" + dataset + "--------------"
        final_path = my_path + dataset
        normal_conn, malware_conn, d = extract_feature(final_path)
        number_of_ssl_M, number_of_ssl_N, number_of_x509_M, number_of_x509_N = \
            find_ssl_log(final_path, d, normal_cer_dict, malware_cer_dict, normal_conn_tuples_dict, malware_conn_tuples_dict)


        number_of_conn_M += malware_conn
        number_of_conn_N += normal_conn
        number_of_ssl_M_tot += number_of_ssl_M
        number_of_ssl_N_tot += number_of_ssl_N

        number_of_x509_M_tot += number_of_x509_M
        number_of_x509_N_tot += number_of_x509_N

    print "-----------------------------------------------------"
    print "---------- Results for all experiments --------------"
    print "-----------------------------------------------------"
    print "Total malware flow from conn.logs:", number_of_conn_M
    print "Total normal flow from conn.logs:", number_of_conn_N
    print "Total malware flow from ssl.logs:", number_of_ssl_M_tot
    print "Total normal flow from ssl.logs:", number_of_ssl_N_tot
    print "Total malware certificate in x509.logs:", len(malware_cer_dict.keys())
    print "Total normal certificate in x509.logs:", len(normal_cer_dict.keys())
    print "Total malware 4-tuples:", len(malware_conn_tuples_dict.keys())
    print "Total normal 4-tuples:", len(normal_conn_tuples_dict.keys())
