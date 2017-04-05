"""
This script tries to find such flow which are not from ssl connection but they use ssl ports (443, ...)
"""
import os


class Feature_15:

    def __init__(self):
        self.conn_dict = dict()
        self.conn_dict_2 = dict()
        self.conn_tuples = dict()
        self.conn_labels = dict()

    def function_manager(self, path):
        # self.conn_dict = dict()

        self.create_all_connections(path)
        self.load_ssl(path)

    def create_all_connections(self, path):

        print "<<< reading conn_label.log"
        with open(path + '\\bro\\conn_label.log') as f:
            for line in f:
                if '#' in line:
                    continue
                split = line.split('	')
                conn_uid = split[1]
                label = split[21]
                dst_port = split[5]

                if 'Background' in label:
                    continue

                if not("From-Botnet" in label) and not("From-Normal" in label):
                    print "Error:", label
                    break

                connection_index = split[2], split[4], split[5], split[6]

                try:
                    self.conn_tuples[connection_index].append(conn_uid)
                except:
                    self.conn_tuples[connection_index] = []
                    self.conn_tuples[connection_index].append(0)
                    self.conn_tuples[connection_index].append(conn_uid)

                try:
                    if self.conn_dict[conn_uid]:
                        print conn_uid
                        print "Error: smae uid"
                        break
                except:
                    self.conn_dict[conn_uid] = connection_index

                try:
                    if self.conn_dict_2[conn_uid]:
                        print conn_uid
                        print "Error: smae uid"
                        break
                except:
                    self.conn_dict_2[conn_uid] = dst_port

                try:
                    if self.conn_labels[conn_uid]:
                        print conn_uid
                        print "Error: smae uid"
                        break
                except:
                    self.conn_labels[conn_uid] = split[21]

        f.close()
        # print len(self.conn_tuples.keys())

    def load_ssl(self, path):
        print "<<< reading ssl.log"
        with open(path + '\\bro\\ssl.log') as f:
            for line in f:
                if '#' in line:
                    continue
                split = line.split('	')
                ssl_uid = split[1]

                try:
                    self.conn_tuples[self.conn_dict[ssl_uid]][0] = 1
                except:
                    pass
        f.close()
        # print len(self.ssl_tuple.keys())

    def evaluate(self):
        print "<<< evaluating"
        ssl_tuples = 0
        all_tuples = 0
        for key in self.conn_tuples.keys():
            if self.conn_tuples[key][0] == 1:
                ssl_tuples += 1
            all_tuples += 1
        print "ssl connection:", ssl_tuples
        print "all connection:", all_tuples

    def checking_443(self):
        port_443_normal = 0
        port_443_malware = 0
        for key in self.conn_dict_2.keys():
            if '443' in self.conn_dict_2[key]:
                connection_index = self.conn_dict[key]
                if self.conn_tuples[connection_index][0] == 0:
                    if "From-Botnet" in self.conn_labels[key]:
                        port_443_malware += 1
                    if "From-Normal" in self.conn_labels[key]:
                        port_443_normal += 1
                    # print key
        print "malware 443 port:", port_443_malware
        print "normal 443 port:", port_443_normal


if __name__ == '__main__':
    my_path = "c:/Users/frenk/Documents/Skola/Bachelor_thesis/datasets/"

    ssl_connection = 0

    datasets = os.listdir(my_path)

    f = Feature_15()
    for dataset in datasets:
        print "----------" + dataset + "--------------"
        final_path = my_path + dataset

        f.function_manager(final_path)

    print "-------- Statistics -----------"
    print "All ssl connection:", f.evaluate()
    print "all flows in conn.log:", len(f.conn_dict_2.keys())
    print "checking 443:", f.checking_443()
