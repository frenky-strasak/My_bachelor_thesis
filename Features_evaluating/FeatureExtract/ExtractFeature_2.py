import os


def extract_feature(path, p_key, usefull_flows):

    conn_dict = dict()
    process_con(path, conn_dict)
    with open(path + "/bro/ssl.log") as f:
        for line in f:
            if '#' in line:
                continue
            split = line.split('	')
            feature = split[1]
            x509_list = split[14]
            try:
                if conn_dict[feature]:
                    usefull_flows[0] += 1
                    if '-' == split[14] or '(object)' == split[14]:
                        print "erroros  "
            except:
                pass


def process_con(path, p_key):
    with open(path + "/bro/conn_label.log") as f:
        for line in f:
            if '#' in line:
                continue
            split = line.split('	')
            feature = split[1]
            label = split[21]
            if 'Botnet' in label or 'Normal' in label:
                try:
                    p_key[feature] += 1
                    print "Error: sracka"
                except:
                    p_key[feature] = 1


def read_result(path):
    flows = 0
    with open(path + "result.txt") as f:
        for line in f:
            split = line.split(",")
            flows += int(split[4])
    f.close()
    print flows

if __name__ == '__main__':
    my_path = "c:/Users/frenk/Documents/Skola/Bachelor_thesis/datasets/"

    datasets = os.listdir(my_path)

    p_key = dict()
    usefull_flows = [0]

    for dataset in datasets:
        print "----------" + dataset + "--------------"
        final_path = my_path + dataset
        extract_feature(final_path, p_key, usefull_flows)

    print usefull_flows

    """
    ---------------------------------------
    """
    # path = "c:/Users/frenk/Documents/Skola/Bachelor_thesis/My_bachelor_thesis/Features_evaluating/PlotData/"
    # read_result(path)