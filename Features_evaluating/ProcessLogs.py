"""
This file goes into logs file and creates "connection 4-tuples" objects.
"""
from PrintManager import __PrintManager__
from EvaluateData import EvaluateData
from Connection_4_tuple import Connection4tuple
# This class, there are all methods for proccessing LogFiles.


class ProcessLogs(EvaluateData):
    def __init__(self, name_of_result):
        super(ProcessLogs, self).__init__()
        self.conn_log = None
        self.name_of_result = name_of_result
        self.ssl_dict = dict()
        self.x509_dict = dict()

    def evaluate_features(self, path_to_dataset):
        self.load_ssl_file(path_to_dataset)
        self.load_x509_file(path_to_dataset)
        self.evaluate_conn_file(path_to_dataset)

    # This method process con.log file.
    # It works inside the opened file, because of large files (such as 70Gb)
    def evaluate_conn_file(self, path_to_dataset):
        __PrintManager__.processLog_evaluating()
        background_flows = 0
        count_lines = 0
        number_adding_ssl = 0
        number_of_adding_x509 = 0
        with open(path_to_dataset + '\\bro\\conn_label.log') as f:
            # go thru file line by line and evaluate each line (line is goodonesIPs)
            for line in f:
                if '#' in line:
                    continue
                count_lines += 1
                split = line.split('	')
                # 2-srcIpAddress, 4-dstIpAddress, 5-dstPort, 6-Protocol
                connection_index = split[2], split[4], split[5], split[6]
                label = split[21]
                conn_uid = split[1]

                if 'Background' in label or 'No_Label' in label:
                    background_flows += 1
                    continue

                try:
                    self.connection_4_tuples[connection_index].add_flow(line, label)
                except:
                    self.connection_4_tuples[connection_index] = Connection4tuple(connection_index)
                    self.connection_4_tuples[connection_index].add_flow(line, label)

                # Find this flow in ssl.log and if find it, add to 4-tuple
                try:
                    ssl_line = self.ssl_dict[conn_uid]

                    # It returns list of x509 which are related with this flow.
                    valid_x509_list = self.split_ssl(ssl_line)
                    number_of_adding_x509 += len(valid_x509_list)

                    self.connection_4_tuples[connection_index].add_ssl_log(ssl_line, valid_x509_list)
                    number_adding_ssl += 1
                except:
                    # this flow does not have ssl log.
                    pass

        f.close()
        self.ssl_dict = dict()
        self.x509_dict = dict()
        # Just pint information about file and 4-tuples and their flows.
        self.count_statistic_of_conn(count_lines, background_flows, number_adding_ssl, number_of_adding_x509)

    '''
    Just checking function, that each x509uid from ssl log is found in x509 file.
    '''
    def split_ssl(self, ssl_line):
        split = ssl_line.split('	')
        if '-' == split[14] or '(object)' == split[14]:
            return []
        return self.get_x509_lines(split[14].split(','))

    def get_x509_lines(self, x509_uids):
        temp_arr = []
        for i in range(len(x509_uids)):
            try:
                if self.x509_dict[x509_uids[i]]:
                    temp_arr.append(self.x509_dict[x509_uids[i]][0])
                    if len(self.x509_dict[x509_uids[i]]) > 1:
                        print "Error: Actual ssl flow needs x509 log, which has more same uids!!!!"
                    # print x509_uids[i]
            except:
                print "Error: In ProcessLogs.py x509 does not have this x509uid:", x509_uids[i]
        return temp_arr

    """
    Just load ssl.log to dictionary
    """
    def load_ssl_file(self, path_to_dataset):
        count_lines = 0
        __PrintManager__.processLog_evaluate_ssl()
        try:
            with open(path_to_dataset + "\\bro\\ssl.log") as f:
                for line in f:
                    if '#' in line:
                        continue
                    split = line.split('	')
                    ssl_uid = split[1]

                    try:
                        if self.ssl_dict[ssl_uid]:
                            print "Error: 2 or more ssl have same flow! Our implentation is base on fact, that every" \
                                  "ssl log belongs to one flow."
                    except:
                        self.ssl_dict[ssl_uid] = line
                    count_lines += 1
            f.close()
        except IOError:
            __PrintManager__.processLog_no_ssl_logs()
        __PrintManager__.processLog_number_of_addes_ssl(count_lines)


    """
    Just load x509.log to dictionary.
    """
    def load_x509_file(self, path_to_dataset):
            count_lines = 0
            try:
                with open(path_to_dataset + "\\bro\\x509.log") as f:
                    # go thru ssl file line by line and for each ssl line check all uid of flows
                    for line in f:
                        if '#' in line:
                            continue
                        split = line.split('	')
                        ssl_uid = split[1]

                        try:
                            self.x509_dict[ssl_uid].append(line)
                            print "Error: more uids in x509!!!", ssl_uid
                        except:
                            self.x509_dict[ssl_uid] = []
                            self.x509_dict[ssl_uid].append(line)

                        count_lines += 1
                f.close()
            except IOError:
                print "Error: No x509 file."
            # print "len dict of x509", len(self.x509_dict)
            __PrintManager__.processLog_number_of_addes_x509(count_lines)

    '''
    ----------------------- Other methods ---------------------------
    '''
    def print_connection_4_tuple(self):
        for key in self.connection_4_tuples.keys():
            self.connection_4_tuples[key].print_features()

    # This method checks error in connection 4-tuple.
    # So if 4-tuple contains some malware flows and some normal goodonesIPs, that is error!!!
    def check_4_tuples(self):
        __PrintManager__.processLog_check_tuples()
        no_variants = 0
        malware_flows = 0
        normal_flows = 0
        for key in self.connection_4_tuples.keys():
            # Count number of all flows.
            if self.connection_4_tuples[key].is_malware():
                malware_flows += self.connection_4_tuples[key].get_number_of_flows()
            else:
                normal_flows += self.connection_4_tuples[key].get_number_of_flows()

            if self.connection_4_tuples[key].get_malware_label() != 0 and \
                            self.connection_4_tuples[key].get_normal_label() != 0:
                    print "Tuple index: ", self.connection_4_tuples[key].tuple_index
                    print "Number of malware: ", self.connection_4_tuples[key].get_malware_label()
                    print "Number of normal: ", self.connection_4_tuples[key].get_normal_label()
                    no_variants += 1

        __PrintManager__.processLog_result_number_of_flows(normal_flows, malware_flows)
        if no_variants == 0:
            __PrintManager__.processLog_result_1_of_check()
        else:
            __PrintManager__.processLog_result_2_of_check()

    # Number of flows for using: normal = 343113  + malware = 338468  = 681581
    def count_statistic_of_conn(self, number_of_lines, background_flows, number_adding_ssl, number_of_adding_x509):
        # Count number of malware 4-tuples and malware 4-tuples for printing statistic.
        malware_tuples = 0
        normal_tuples = 0
        malware_flows = 0
        normal_flows = 0

        for key in self.connection_4_tuples.keys():

            if self.connection_4_tuples[key].get_uid_flow_dict_length() != self.connection_4_tuples[key].get_number_of_flows():
                    print "Error: dict and array are not same !!!!!"

            if self.connection_4_tuples[key].is_malware():
                malware_tuples += 1
                malware_flows += self.connection_4_tuples[key].get_number_of_flows()
            else:
                normal_tuples += 1
                normal_flows += self.connection_4_tuples[key].get_number_of_flows()

        __PrintManager__.processLog_evaluating2(malware_flows,normal_flows, background_flows,
                                                len(self.connection_4_tuples),
                                                normal_tuples, malware_tuples, number_of_lines, number_adding_ssl, number_of_adding_x509)