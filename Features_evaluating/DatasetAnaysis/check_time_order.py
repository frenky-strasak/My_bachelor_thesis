import sys
import os




def read_conn(path):
    con_dict = dict()

    t1 = 0
    t2 = 0
    with open(path + "/bro/conn_label.log") as f:
        for line in f:
            if '#' == line[0]:
                continue
            split = line.split('	')
            uid = split[1]
            time = split[0]
            if t2 == 0:
                t2 = time
                continue

            t1 = t2
            t2 = time

            if t2 < t1:
                print "The time is not in order."
                print "t1:", t1
                print "t2:", t2
                f.close()
                return

    f.close()


if __name__ == '__main__':

    if len(sys.argv) > 1:
        my_path = sys.argv[1]

        datasets = os.listdir(my_path)
        d = dict()
        for dataset in datasets:
            print "-----", dataset, "------"
            read_conn(my_path + dataset)


    else:
        print "Error: wrong arguments."