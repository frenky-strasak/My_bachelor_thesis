import sys

def read_conn(path):
    d = dict()
    infected_ips = dict()
    line_number = 0
    with open(path + "bro/conn.log") as f:
        for line in f:
            line_number += 1
            if '#' == line[0]:
                continue
            split = line.split('	')
            try:
                src_address = split[2]
            except:
                print "--------------"
                print line
                print line_number
                print "--------------"
            # label = split[21]
            # if 'From-Botnet' in label:
            #     try:
            #         infected_ips[src_address] += 1
            #     except:
            #         infected_ips[src_address] = 1


            try:
                d[src_address] += 1
            except:
                d[src_address] = 1
    f.close()
    print d
    print line_number
    # print infected_ips.keys()



if __name__ == '__main__':
    if len(sys.argv) == 2:
        path = sys.argv[1]
        read_conn(path)