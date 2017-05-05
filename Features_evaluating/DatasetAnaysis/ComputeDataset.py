import sys
import os
from time import time

class ComputeDatasets:
    def __init__(self):
        # self.connection_4_tuples = dict()
        self.conn_dict = dict()

        self.tuple_malware = dict()
        self.tuple_normal = dict()

        self.conn_malware = 0
        self.conn_normal = 0

        self.ssl_malware = 0
        self.ssl_normal = 0

        self.x509_malware = 0
        self.x509_normal = 0

    def manager(self, path):
        self.conn_dict = dict()
        # self.connection_4_tuples = dict()

        self.read_conn(path)
        self.read_ssl(path)

    def read_conn(self, path):
        print "<< conn.log:"
        normal = 0
        malware = 0
        index = 0
        with open(path + "/bro/conn_label.log") as f:
            for line in f:
                if '#' == line[0]:
                    continue
                split = line.split('	')

                label = split[21]
                if 'Background' in label or 'No_Label' in label:
                    continue

                # try:
                #     if self.conn_dict[split[1]]:
                #         print "Error: more uids in conn.log!!!!!!!11"
                # except:
                #     # self.conn_dict[split[1]] = split[21]
                #     self.conn_dict[split[1]] = line

                self.conn_dict[split[1]] = line

                # connection_index = split[2], split[4], split[5], split[6]
                # try:
                #     if self.connection_4_tuples[split[1]]:
                #         print "Error: more uids in conn.log!!!!!!!11"
                # except:
                #     self.connection_4_tuples[split[1]] = connection_index

                if "From-Botnet" in split[21]:
                    malware += 1
                if "From-Normal" in split[21]:
                    normal += 1
                index += 1

                if index % 100000 == 0:
                    print index
        f.close()

        print "Malware flows in conn.log:", malware
        print "Normal flows in conn.log:", normal
        print "Number of lines in conn.log:", index
        self.conn_malware += malware
        self.conn_normal += normal

    def read_ssl(self, path):
        print "<< ssl.log:"

        number_of_ssl_M = 0
        number_of_ssl_N = 0
        number_of_x509_M = 0
        number_of_x509_N = 0

        index = 0

        ssl_dict = dict()

        with open(path + "/bro/ssl.log") as f:
            for line in f:
                if '#' == line[0]:
                    continue

                index += 1
                split = line.split('	')
                ssl_uid = split[1]
                try:
                    if ssl_dict[ssl_uid]:
                        continue
                except:
                    ssl_dict[ssl_uid] = 1

                try:
                    conn_split = self.conn_dict[split[1]].split('	')
                    label = conn_split[21]
                    connection_key = conn_split[2], conn_split[4], conn_split[5], conn_split[6]
                except:
                    continue

                # label = self.conn_dict[split[1]].split('	')[21]
                if "Background" in label:
                    print "Error: mrte divny"
                    continue

                # connection_key = self.connection_4_tuples[split[1]]
                if "From-Botnet" in label:
                    number_of_ssl_M += 1
                    try:
                        self.tuple_malware[connection_key] += 1
                    except:
                        self.tuple_malware[connection_key] = 1

                if "From-Normal" in label:
                    number_of_ssl_N += 1
                    try:
                        self.tuple_normal[connection_key] += 1
                    except:
                        self.tuple_normal[connection_key] = 1

                if split[14] == '-':
                    continue

                if "From-Botnet" in label:
                    number_of_x509_M += 1

                if "From-Normal" in label:
                    number_of_x509_N += 1
        f.close()

        print "Malware flows in ssl.log:", number_of_ssl_M
        print "Normal flows in ssl.log:", number_of_ssl_N
        print "Number of lines in ssl.log:", index
        print "Malware certificates(lines) in x509 from ssl.log:", number_of_x509_M
        print "Normal certificates(lines) in x509 from ssl.log:", number_of_x509_N

        self.ssl_malware += number_of_ssl_M
        self.ssl_normal += number_of_ssl_N

        self.x509_malware += number_of_x509_M
        self.x509_normal += number_of_x509_N


if __name__ == '__main__':
    if len(sys.argv) > 1:
        my_path = sys.argv[1]

        cmp = ComputeDatasets()

        datasets = os.listdir(my_path)
        t0 = time()
        index = 0
        for dataset in datasets:
            index += 1
            print "---------- " +str(index)+"/"+ str(len(datasets))+ " " + dataset + "--------------"
            final_path = my_path + dataset

            cmp.manager(final_path)


        print "-----------------------------------------------------"
        print "---------- Results for all experiments --------------"
        print "-----------------------------------------------------"
        print "Total malware flow from ssl.logs:", cmp.ssl_malware
        print "Total normal flow from ssl.logs:", cmp.ssl_normal
        print "Total malware certificate in x509.logs:", cmp.x509_malware
        print "Total normal certificate in x509.logs:", cmp.x509_normal
        print "Total malware connections", len(cmp.tuple_malware.keys())
        print "Total normal connections", len(cmp.tuple_normal.keys())

        t1 = time()
        print "<<< All dataset successfully finished in aproximate time: %f" % ((t1 - t0) / 60.0) + " min."