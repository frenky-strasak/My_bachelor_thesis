import ComputeFeatures
# This class, there are all methods for proccessing LogFiles.


class ProcessLog:
    def __init__(self, path_to_folder, infected_ips_list):
        self.path_to_folder = path_to_folder
        self.infected_ips_list = infected_ips_list
        self.connection_4_tuple = dict()
        self.conn_log = None
        self.karel = 0

    def evaluate_features(self):
        self.evaluate_conn_file()
        self.evaluate_ssl_file()

    # This method process con.log file.
    # It works inside the opened file, because of large files (such as 70Gb)
    def evaluate_conn_file(self):
        print "<< ProcessLog.py: Evaluating of conn file..."
        with open(self.path_to_folder + '\\bro\\conn.log') as f:
            # go thru file line by line and evaluate each line (line is flow)
            for line in f:
                if '#' in line:
                    continue
                split = line.split('	')
                # 2-srcIpAddress, 4-dstIpAddress, 5-dstPort, 6-Protocol
                connection_index = split[2], split[4], split[5], split[6]
                ipaddresses = split[2], split[4]
                ipaddresses_reverse = split[4], split[2]

                if connection_index not in self.connection_4_tuple.keys():
                    self.connection_4_tuple[connection_index] = ComputeFeatures.ComputeFeatures(connection_index)

                if ipaddresses in self.infected_ips_list:
                    self.connection_4_tuple[connection_index].add_flow(line, "MALWARE")
                else:
                    self.connection_4_tuple[connection_index].add_flow(line, "NORMAL")

        f.close()

    def evaluate_ssl_file(self):
        print "<< ProcessLog.py: Evaluating of ssl file..."
        # jeden 4Tuple ma spousta flows ... jeden flows ma jeden uid, takze jeden 4-tuple ma spoustu uid
        with open(self.path_to_folder + "\\bro\\ssl.log") as f:
            # go thru ssl file line by line and for each ssl line check all uid of flows
            number_adding_ssl = 0
            for line in f:
                if '#' in line:
                    continue
                split = line.split('	')
                ssl_uid = split[1]

                for key in self.connection_4_tuple.keys():
                    if ssl_uid in self.connection_4_tuple[key].get_uid_flow_list():
                        self.connection_4_tuple[key].add_ssl_log(line)
                        number_adding_ssl += 1

        # print "Pocet pridanych ssl logu: ", number_adding_ssl

    def print_connection_4_tuple(self):
        for key in self.connection_4_tuple.keys():
            self.connection_4_tuple[key].print_features()

    # This method checks error in connection 4-tuple.
    # So if 4-tuple contains some malware flows and some normal flow, that is error!!!
    def check_4_tuples(self):
        print "<< ProcessLogs.py: Checking connections..."
        no_variants = 0
        for key in self.connection_4_tuple.keys():
            if self.connection_4_tuple[key].get_malware_label() != 0 and \
                            self.connection_4_tuple[key].get_normal_label() != 0:
                    print "Tuple index: ", self.connection_4_tuple[key].tuple_index
                    print "Number of malware: ", self.connection_4_tuple[key].get_malware_label()
                    print "Number of normal: ", self.connection_4_tuple[key].get_normal_label()
                    no_variants += 1

        if no_variants == 0:
            print "     << ProcessLog.py: Connections are ok. Each connection has 0 malwares or 0 normal."

    def get_size_of_con4tuple(self):
        return len(self.connection_4_tuple)


