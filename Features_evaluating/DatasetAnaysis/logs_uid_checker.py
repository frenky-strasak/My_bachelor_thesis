import sys
import os

def read_ssl(path, conn_dict):

    d = dict()
    with open(path + "/bro/ssl.log") as f:
        for line in f:
            if '#' == line[0]:
                continue
            split = line.split('	')
            uid = split[1]

            try:
                label = conn_dict[uid]
            except:
                continue


            if "Background" in label:
                print "Error neco spatne more..."
                continue

            try:
                d[uid] += 1
                # if d[uid]:
                    # print "Error: more uids in conn.log!!!!!!!"
                print uid
            except:
                d[uid] = 1
    f.close()

    total = 0
    for key in d.keys():
        total += d[key]

    print "length keys of uid in ssl.log:", len(d.keys())
    print "number of lines in ssl:", total


def read_conn(path):
    con_dict = dict()

    with open(path + "/bro/conn_label.log") as f:
        for line in f:
            if '#' == line[0]:
                continue
            split = line.split('	')
            uid = split[1]
            label = split[21]

            if "Background" in label:
                continue

            try:
                if con_dict[uid]:
                    print "Error: more uids in conn.log!!!!!!!"
            except:
                con_dict[uid] = label

    f.close()
    return con_dict


if __name__ == '__main__':

    if len(sys.argv) > 1:
        my_path = sys.argv[1]

        datasets = os.listdir(my_path)
        d = dict()
        for dataset in datasets:
            print "-----", dataset, "------"
            d = read_conn(my_path + dataset)
            read_ssl(my_path + dataset, d)

    else:
        print "Error: wrong arguments."