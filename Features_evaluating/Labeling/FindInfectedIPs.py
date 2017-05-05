import sys
import os
from netaddr import *


def read_ssl(path_to_dataset):
    infected_ips = dict()

    with open(path_to_dataset + '\\bro\\ssl.log') as f:
        for line in f:
            if '#' == line[0]:
                continue
            split = line.split('	')
            src_address = split[2]

            try:
                infected_ips[src_address] += 1
            except:
                infected_ips[src_address] = 1
    f.close()
    print "<<<<<<< SSL.LOG <<<<<<<<<<<"
    print "<<< All srcIPs:"
    print infected_ips
    print "<<< Private ips:"
    for ip in infected_ips.keys():
        if IPAddress(ip).is_private:
            print ip

def read_conn(path_to_dataset):
    infected_ips = dict()

    with open(path_to_dataset + '\\bro\\conn.log') as f:
        for line in f:
            if '#' == line[0]:
                continue
            split = line.split('	')
            src_address = split[2]

            try:
                infected_ips[src_address] += 1
            except:
                infected_ips[src_address] = 1
    f.close()
    print "<<<<<<< CONN.LOG <<<<<<<<<<<"
    print "<<< All srcIPs:"
    print infected_ips
    print "<<< Private ips:"
    for ip in infected_ips.keys():
        if IPAddress(ip).is_private:
            print ip




def dataset_manager():
    path = "c:/Users/frenk/Documents/Skola/Bachelor_thesis/Dataset/MALWARE/dataset_1-168/without_bro/"
    for dir in os.listdir(path):
        print "--------------- ", dir, "--------------------------------"
        # read_conn(path + dir)
        read_ssl(path + dir)


if __name__ == '__main__':

    # print IPAddress('74.125.236.194').is_private()

    if len(sys.argv) == 2:
        path = sys.argv[1]

        """
        For single dataset
        """
        read_conn(path)
        read_ssl(path)

    """
    For finding in datasets folder
    """
    # dataset_manager()