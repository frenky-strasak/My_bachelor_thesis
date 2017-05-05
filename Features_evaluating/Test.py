import sys

def read_conn(path):
    d = dict()
    infected_ips = dict()
    line_number = 0
    with open(path + "bro/x509.log") as f:
        for line in f:
            line_number += 1
            if '#' == line[0]:
                continue
            split = line.split('	')
            print split[14]
            san_dns = split[14].split(',')
            for i in range(len(san_dns)):
                if '*' in san_dns[i]:
                    san_dns[i] = san_dns[i].replace('*', '')
            print san_dns
            break
    f.close()



if __name__ == '__main__':
    # if len(sys.argv) == 2:
    #     path = sys.argv[1]
    #     read_conn(path)


    arr = [1,2,3,4,5,6]

    for a in arr:
        if a == 4:
            print "prt"