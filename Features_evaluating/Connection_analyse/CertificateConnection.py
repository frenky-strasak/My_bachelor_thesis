"""
This script rads 2 files, "malware_ssl_logs.txt" and "normal_ssl_logs.txt". It computes based statistic such as:
number of malware ssl logs which don't have server name, etc.
"""


"""
read malware_ssl_logs.txt
"""
all_M = 0
no_server_name_ssl_logs_M = 0
no_x509_ssl_logs_M = 0
no_x509_and_no_server_name_ssl_logs_M = 0

all_N = 0
no_server_name_ssl_logs_N = 0
no_x509_ssl_logs_N = 0
no_x509_and_no_server_name_ssl_logs_N= 0

cert_info_M = 0
cert_info_N = 0

new_conn = 0
index = 0
conn_name = ''
temp_big = 0
temp = 0

malware_number = 0
with open("malware_ssl_logs.txt") as f:

    for line in f:
        if line == '\n':
            continue

        if '#' in line:
            if index != 0 and new_conn == index:
                # print "This connection ", conn_name, "has no information about certificate"
                cert_info_M += 1
            if temp != 0:
                temp_big += 1
            new_conn = 0
            index = 0
            split = line.split(" ")
            conn_name = split[4], split[5], split[6], split[7]
            temp = 0
            malware_number += 1
            continue

        split = line.split('	')

        server_name = split[9]
        x509_uids = split[14]

        if server_name != '-' and x509_uids != '-':
            all_M += 1
            print line
            temp += 1
        if server_name == '-' and x509_uids != '-':
            no_server_name_ssl_logs_M += 1
            print line
            temp += 1
        if server_name != '-' and x509_uids == '-':
            # print line
            no_x509_ssl_logs_M += 1
            print line
            temp += 1
        if server_name == '-' and x509_uids == '-':
            no_x509_and_no_server_name_ssl_logs_M += 1
            new_conn += 1

        index += 1

f.close()

new_conn = 0
index = 0
conn_name = ''
with open("normal_ssl_logs.txt") as f:

    for line in f:
        if line == '\n':
            continue

        if '#' in line:
            if index != 0 and new_conn == index:
                # print "This connection ", conn_name, "has no information about certificate"
                cert_info_N += 1
            new_conn = 0
            index = 0
            split = line.split(" ")
            conn_name = split[4], split[5], split[6], split[7]
            continue

        split = line.split('	')
        server_name = split[9]
        x509_uids = split[14]

        if server_name != '-' and x509_uids != '-':
            all_N += 1
        if server_name == '-' and x509_uids != '-':
            no_server_name_ssl_logs_N += 1
        if server_name != '-' and x509_uids == '-':
            no_x509_ssl_logs_N += 1
        if server_name == '-' and x509_uids == '-':
            # print line
            no_x509_and_no_server_name_ssl_logs_N += 1
            new_conn += 1
        index += 1

f.close()

print "Malwares:"
print "Some server , some x509 M:", all_M
print "no server name, some uids M:", no_server_name_ssl_logs_M
print "some server name, no x509 M:", no_x509_ssl_logs_M
print "no x509, no server name M:", no_x509_and_no_server_name_ssl_logs_M
print "number of connection which has no info about cert.:", cert_info_M
print "number of connection which has some info about cert.", temp_big
print "number of malware:", malware_number

print "Normals:"
print "Some server , some x509 N:", all_N
print "no server name, some uids N:", no_server_name_ssl_logs_N
print "some server name, no x509 N:", no_x509_ssl_logs_N
print "noc x509, no server name N:", no_x509_and_no_server_name_ssl_logs_N
print "number of connection which has no info about cert.:", cert_info_N