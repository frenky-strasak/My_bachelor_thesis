"""
This file goes into logs file and creates "connection 4-tuples" objects.
"""
from PrintManager import __PrintManager__
from EvaluateData import EvaluateData
from Connection_4_tuple import Connection4tuple
from CertificatesSerial import CertificateSerial
import os


class ProcessLogs(EvaluateData):
    def __init__(self, name_of_result):
        super(ProcessLogs, self).__init__()
        self.name_of_result = name_of_result
        self.x509_dict = dict()
        self.con_dict = dict()


        self.not_added_x509 = 0

        self.is_computed_443feature = False
        self.all_conn_dict = dict()
        self.control_ssl_uids_dict = dict()

        self.number_ssl_logs = 0
        self.number_x509_logs = 0

    def evaluate_features(self, path_to_dataset):
        self.load_x509_file(path_to_dataset)
        self.load_conn_file(path_to_dataset)
        self.create_4_tuples(path_to_dataset)

        self.add_not_ssl_logs(path_to_dataset)



    '''
    This method goes thru ssl file and creates 4-tuples
    '''
    def create_4_tuples(self, path_to_dataset):
        background_flows = 0
        number_of_adding_x509 = 0
        number_adding_ssl = 0
        count_lines = 0

        self.not_added_x509 = 0

        # file_hitrate = 0

        with open(path_to_dataset + "\\bro\\ssl.log") as ssl_file:
            for ssl_line in ssl_file:
                if '#' == ssl_line[0]:
                    continue
                count_lines += 1

                ssl_split = ssl_line.split('	')
                ssl_uid = ssl_split[1]

                # if same ssl, continue (in some ssl.log files are more same ssl lines. It is probably bro error)
                try:
                    if self.control_ssl_uids_dict[ssl_uid]:
                        continue
                except:
                    self.control_ssl_uids_dict[ssl_uid] = 1

                # find flow in conn.log by this ssl uid.
                try:
                    conn_log = self.con_dict[ssl_uid]
                except:
                    # print "Error: ssl log does not have conn log !!!"
                    # break
                    continue

                conn_split = conn_log.split('	')
                # 2-srcIpAddress, 4-dstIpAddress, 5-dstPort, 6-Protocol
                connection_index = conn_split[2], conn_split[4], conn_split[5], conn_split[6]
                try:
                    label = conn_split[21]
                except IndexError:
                    print "Error: no label in conn line."

                if 'Background' in label or 'No_Label' in label:
                    background_flows += 1
                    print "Error: Sakra divny."
                    continue

                if not('Botnet' in label) and not('Normal') in label:
                    print "Error: Dear more, there are more states of labels !!!!"

                # file_hitrate += self.find_uid(path_to_dataset, ssl_uid)


                try:
                    self.connection_4_tuples[connection_index].add_ssl_flow(conn_log, label)
                except:
                    self.connection_4_tuples[connection_index] = Connection4tuple(connection_index)
                    self.connection_4_tuples[connection_index].add_ssl_flow(conn_log, label)

                # x509 and ssl
                valid_x509_list = self.split_ssl(ssl_line, connection_index, label)
                number_of_adding_x509 += len(valid_x509_list)

                self.connection_4_tuples[connection_index].add_ssl_log(ssl_line, valid_x509_list, os.path.basename(path_to_dataset))
                number_adding_ssl += 1

                # --------- just for printing for sebas -------
                self.number_ssl_logs += 1
                self.number_x509_logs += len(valid_x509_list)



        ssl_file.close()


        self.con_dict = dict()
        self.x509_dict = dict()
        self.control_ssl_uids_dict = dict()
        # Just pint information about file and 4-tuples and their flows.
        self.count_statistic_of_conn(count_lines, background_flows, number_adding_ssl, number_of_adding_x509)
        # print "number_not_adding_ssl", self.not_added_x509


    """
    Load conn.log to dictionary
    """
    def load_conn_file(self, path_to_dataset):
        with open(path_to_dataset + '\\bro\\conn_label.log') as f:
            for line in f:
                if '#' == line[0]:
                    continue
                split = line.split('	')
                conn_uid = split[1]
                label = split[21]
                if 'Background' in label or 'No_Label' in label:
                    continue
                try:
                    if self.con_dict[conn_uid]:
                        print "Error: There are more conn log with same uid !!!"
                except:
                    self.con_dict[conn_uid] = line
                # self.con_dict[conn_uid] = line
        f.close()


    """
    Just load x509.log to dictionary.
    """
    def load_x509_file(self, path_to_dataset):
        """
         Read started_file.txt where is time when capture of this dataset starts. Some datasets have starting 
         time 1.1. 1970 00:00:00. So we have to add to time 
         If this file does not exist, dataset has right format time.
        """
        started_unix_time = 0.0
        try:
            with open(path_to_dataset + "\\start_date.txt") as f:
                started_unix_time = float(f.readlines()[1])
            f.close()
        except:
            pass

        count_lines = 0
        try:
            with open(path_to_dataset + "\\bro\\x509.log") as f:
                # go thru ssl file line by line and for each ssl line check all uid of flows
                for line in f:
                    if '#' == line[0]:
                        continue
                    split = line.split('	')

                    """
                    Change time, because some datasets are from 1.1 1970 00:00:00.
                    """
                    time_new = float(split[0]) + started_unix_time
                    new_line = str(time_new)
                    for i in range(1, len(split)):
                        new_line += '	' + split[i]

                    x509_uid = split[1]
                    try:
                        self.x509_dict[x509_uid].append(new_line)
                        # print "Error: [load function] more uids in x509!!!", x509_uid
                    except:
                        self.x509_dict[x509_uid] = []
                        self.x509_dict[x509_uid].append(new_line)

                    count_lines += 1
            f.close()
        except IOError:
            print "Error: No x509 file."
        # print "len dict of x509", len(self.x509_dict)
        # __PrintManager__.processLog_number_of_addes_x509(count_lines)


    '''
    Methods for adding not ssl flow from conn.log to connection-4tuple
    '''
    def add_not_ssl_logs(self, path_to_dataset):
        print "     <<< adding not ssl flow:"
        not_ssl_conn = 0
        ssl_conn = 0
        no_idea = 0
        malicious_flows = 0
        with open(path_to_dataset + '\\bro\\conn_label.log') as f:
            for line in f:
                if '#' == line[0]:
                    continue
                conn_split = line.split('	')
                # 2-srcIpAddress, 4-dstIpAddress, 5-dstPort, 6-Protocol
                connection_index = conn_split[2], conn_split[4], conn_split[5], conn_split[6]
                try:
                    label = conn_split[21]
                except IndexError:
                    label = "False"
                conn_uid = conn_split[1]

                if 'Background' in label or 'No_Label' in label:
                    continue

                try:
                    if self.connection_4_tuples[connection_index]:
                        try:
                            if self.connection_4_tuples[connection_index].get_uid_flow_dict()[conn_uid]:
                                ssl_conn += 1
                        except:
                            self.connection_4_tuples[connection_index].add_not_ssl_flow(line, label)
                            not_ssl_conn += 1
                except:
                    # Connections which are normal or botnet but they don't have ssl 4-tuple object.
                    pass

        f.close()

        print "          <<< not ssl conn:", not_ssl_conn
        print "          <<< ssl conn:", ssl_conn
        # print "          <<< con without ssl 4-tuple object:", no_idea


    '''
    ----------------------- Other methods ---------------------------
    '''

    '''
    Just checking function, that each x509uid from ssl log is found in x509 file.
    '''
    def split_ssl(self, ssl_line, tuple_index, label):
        split = ssl_line.split('	')
        if '-' == split[14] or '(object)' == split[14]:
            self.not_added_x509 += 1
            return []
        self.put_server_name_to_dict(split[1], split[9], tuple_index, split[14], label)
        return [self.get_x509_lines(split[14].split(','))]

    '''
    This function returns x509 line which ssl log has inside his line as list of uid.
    '''
    def get_x509_lines(self, x509_uids_list):
        x509_line = None
        uid_x509 = x509_uids_list[0]
        try:
            if self.x509_dict[uid_x509]:
                # x509_dict is array. So [0] is the reason.
                x509_line = self.x509_dict[uid_x509][0]
                if len(self.x509_dict[uid_x509]) > 1:
                    print "Error: [ProcessLogs] Actual ssl flow needs x509 log, which has more same uids!!!!"
                # print x509_uids_list[i]
        except:
            print "Error: [get_x509_lines] In ProcessLogs.py x509 does not have this x509uid:", x509_uids_list[0]
        return x509_line

    # certificate dict
    def put_server_name_to_dict(self, ssl_uid, server_name, tuple_index, x509_uids_list, label):
        splited_x509_uids = x509_uids_list.split(',')
        uid_x509 = splited_x509_uids[0]
        try:
            if self.x509_dict[uid_x509]:
                x509_line = self.x509_dict[uid_x509][0]
                x509_split = x509_line.split('	')
                cert_serial = x509_split[3]
                try:
                    if self.certificate_dict[cert_serial]:
                        self.certificate_dict[cert_serial].add_server_name(server_name, label)
                        self.certificate_dict[cert_serial].add_x509_line(x509_line)
                except:
                    self.certificate_dict[cert_serial] = CertificateSerial(cert_serial, x509_line)
                    self.certificate_dict[cert_serial].add_server_name(server_name, label)
                    self.certificate_dict[cert_serial].add_x509_line(x509_line)
        except:
            print "Error: [put_server_name] In ProcessLogs.py x509 does not have this x509uid:", uid_x509

    """
    ---------------------------------------------------------------------------------
    """
    def print_connection_4_tuple(self):
        for key in self.connection_4_tuples.keys():
            self.connection_4_tuples[key].print_features()

    """
     -------------------- check_4_tuples --------------------------------
    """

    # This method checks error in connection 4-tuple.
    # So if 4-tuple contains some malware flows and some normal goodonesIPs, that is error!!!
    def check_4_tuples(self):
        __PrintManager__.processLog_check_tuples()
        no_variants = 0
        all_malware_flows = 0
        all_normal_flows = 0
        ssl_malware_flows = 0
        not_ssl_malware_flows = 0
        ssl_normal_flows = 0
        not_ssl_normal_flows = 0
        normal_cert = 0
        malware_cert = 0
        normal_connections = 0
        malware_connections = 0
        for key in self.connection_4_tuples.keys():

            """
            implementig feature: connection which have no certificate, but have at least one SNI,
            look, if in certificate_objects_dict is such servername with certificate
            """
            break_v = 0
            if self.connection_4_tuples[key].get_amount_diff_certificates() == 0:

                server_names = self.connection_4_tuples[key].get_SNI_list()
                if len(server_names) != 0:
                    for cert_serial in self.certificate_dict.keys():
                        for server_name in server_names:
                            x509_line = self.certificate_dict[cert_serial].contain_server_name(server_name)
                            if x509_line != 0:
                                self.connection_4_tuples[key].add_ssl_log_2(x509_line)
                                print "This Certificate was added after process:", "cert_serial:", cert_serial, "server_name=",server_name, "4-tuple=", key,\
                                    "label:", self.connection_4_tuples[key].get_label_of_connection()
                                break_v = 1
                                break
                        if break_v == 1:
                            break


            # Count number of all flows.
            if self.connection_4_tuples[key].is_malware():
                all_malware_flows += self.connection_4_tuples[key].get_number_of_flows()
                ssl_malware_flows += self.connection_4_tuples[key].get_number_of_ssl_flows()
                not_ssl_malware_flows += self.connection_4_tuples[key].get_number_of_not_ssl_flows()
                malware_cert += self.connection_4_tuples[key].get_amount_diff_certificates()
                malware_connections += 1
            else:
                all_normal_flows += self.connection_4_tuples[key].get_number_of_flows()
                ssl_normal_flows += self.connection_4_tuples[key].get_number_of_ssl_flows()
                not_ssl_normal_flows += self.connection_4_tuples[key].get_number_of_not_ssl_flows()
                normal_cert += self.connection_4_tuples[key].get_amount_diff_certificates()
                normal_connections += 1

            if self.connection_4_tuples[key].get_malware_label() != 0 and \
                            self.connection_4_tuples[key].get_normal_label() != 0:
                    print "Tuple index: ", self.connection_4_tuples[key].tuple_index
                    print "Number of malware: ", self.connection_4_tuples[key].get_malware_label()
                    print "Number of normal: ", self.connection_4_tuples[key].get_normal_label()
                    no_variants += 1

        # __PrintManager__.processLog_result_number_of_flows(normal_flows, malware_flows)
        space_1 = "     "
        space_2 = "         "
        print space_1 + "<<< Used flows in all connections:"
        print space_2 + "<<< Malwares:"
        print space_2 + "<<< all malware flows:", all_malware_flows
        print space_2 + "<<< ssl malware flows:", ssl_malware_flows
        print space_2 + "<<< NOT ssl malware flows:", not_ssl_malware_flows
        print space_2 + "<<< Normal:"
        print space_2 + "<<< all normal flows:", all_normal_flows
        print space_2 + "<<< ssl normal flows:", ssl_normal_flows
        print space_2 + "<<< NOT ssl normal flows:", not_ssl_normal_flows
        print space_2 + "<<< Certificates"
        print space_2 + "<<< number of normal certificate:", normal_cert
        print space_2 + "<<< number of malware certificate:", malware_cert
        print space_2 + "<<< Connections:"
        print space_2 + "<<< number of normal connection:", normal_connections
        print space_2 + "<<< number of malware connection:", malware_connections

        if no_variants == 0:
            __PrintManager__.processLog_result_1_of_check()
        else:
            __PrintManager__.processLog_result_2_of_check()

        # print Feature
        # self.print_feature_manager()
        # self.print_certificate_and_tuples()
        # self.print_certificate_and_tuples()
        print "ssl together:", self.number_ssl_logs
        print "x509 together:", self.number_x509_logs
        print "number of connection:",len(self.connection_4_tuples.keys())


    """
     -------------------- check_4_tuples --------------------------------
    """

    def print_certificates(self):
        print "\n------------------------------ Certificates info ------------------------------"
        normal_certificate = 0
        malware_certificate = 0
        for key in self.certificate_dict.keys():
            # print "--------------", key, "--------------------------"
            if self.certificate_dict[key].is_malware():
                malware_certificate += 1
            else:
                normal_certificate += 1

        print "normal_certificate:", normal_certificate
        print "malware_certificate:", malware_certificate


    # Number of flows for using: normal = 343113  + malware = 338468  = 681581
    def count_statistic_of_conn(self, number_of_lines, background_flows, number_adding_ssl, number_of_adding_x509):
        # Count number of malware 4-tuples and malware 4-tuples for printing statistic.
        malware_tuples = 0
        normal_tuples = 0
        malware_flows = 0
        normal_flows = 0

        for key in self.connection_4_tuples.keys():

            # print self.connection_4_tuples[key].get_datsets_names_list()

            if self.connection_4_tuples[key].get_uid_flow_dict_length() != self.connection_4_tuples[key].get_number_of_flows():
                    print "Error: dict and array are not same !!!!!"
                    print self.connection_4_tuples[key].get_uid_flow_dict()
                    # print self.connection_4_tuples[key].get_uid_flow_dict()


            if self.connection_4_tuples[key].is_malware():
                malware_tuples += 1
                malware_flows += self.connection_4_tuples[key].get_number_of_flows()
            else:
                normal_tuples += 1
                normal_flows += self.connection_4_tuples[key].get_number_of_flows()
        # malware_flows, normal_flows, malware_tuples, normal_tuples, number_adding_ssl, number_of_adding_x509
        __PrintManager__.processLog_evaluating2(malware_flows, normal_flows, malware_tuples, normal_tuples,
                                                number_adding_ssl, number_of_adding_x509)



    """
    Print all certififivates and which tuple they have.
    """
    def print_certificate_and_tuples(self):
        __PrintManager__.print_header_certificates()
        cert_number = 0
        for key in self.certificate_dict.keys():
            print "Certificate:", key
            normal_labels = 0
            malware_labels = 0
            temp_list = self.certificate_dict[key].get_tuple_index_list()
            for i in range(0, len(temp_list)):
                if self.connection_4_tuples[temp_list[i]].is_malware():
                    print "     Malware:", temp_list[i], self.certificate_dict[key].get_server_names_dict()[temp_list[i]]
                    malware_labels += 1
                else:
                    print "     Normal:", temp_list[i], self.certificate_dict[key].get_server_names_dict()[temp_list[i]]
                    normal_labels += 1
            print "Normal labels:", normal_labels
            print "Malware labels:", malware_labels
            cert_number += 1
        print "certificates number:", cert_number


    """
    Print all certificates.
    """
    def print_certificate_serial_dict(self):
        __PrintManager__.print_header_certificates()
        for key in self.certificate_dict.keys():
            if self.certificate_dict[key].get_size_servers_list() > 1:
                print "----------------------------------------------------------"
                for i in range(0, len(self.certificate_dict[key].get_server_names_list())):
                    print self.certificate_dict[key].get_server_names_list()[i], key

    """
    Print connection feature which are as dictionary. For develop.
    """

    def print_feature_manager(self):

        __PrintManager__.print_header_features_printed()

        self.print_ver_cipher_dict()
        self.print_state_dict()
        self.print_cert_key_length_dict()
        self.print_version_of_ssl_dict()
        self.print_certificate_serial()

    # print ver cipher
    def print_ver_cipher_dict(self):
        print "---------------------------------------------------------"
        print "----- SSL/TLS cipher suite that the server chose. -------"
        conn_logs = 0
        ssl_logs = 0
        cipher_suite_dict = dict()
        for key in self.connection_4_tuples.keys():
            conn_logs += self.connection_4_tuples[key].get_number_of_flows()
            ssl_logs += self.connection_4_tuples[key].get_number_of_ssl_logs()
            for a in self.connection_4_tuples[key].get_ver_cipher_dict().keys():
                try:
                    cipher_suite_dict[a] += self.connection_4_tuples[key].get_ver_cipher_dict()[a]
                except:
                    cipher_suite_dict[a] = self.connection_4_tuples[key].get_ver_cipher_dict()[a]
        print cipher_suite_dict
        print "conn_logs", conn_logs
        print "ssl_logs", ssl_logs

    def print_state_dict(self):
        print "---------------------------------------------------------"
        print "----- State of connections -------"
        conn_logs = 0
        ssl_logs = 0
        temp_dict = dict()
        for key in self.connection_4_tuples.keys():
            conn_logs += self.connection_4_tuples[key].get_number_of_flows()
            ssl_logs += self.connection_4_tuples[key].get_number_of_ssl_logs()
            for a in self.connection_4_tuples[key].get_states_dict().keys():
                try:
                    temp_dict[a] += self.connection_4_tuples[key].get_states_dict()[a]
                except:
                    temp_dict[a] = self.connection_4_tuples[key].get_states_dict()[a]
        print temp_dict
        print "conn_logs", conn_logs
        print "ssl_logs", ssl_logs

    def print_cert_key_length_dict(self):
        print "---------------------------------------------------------"
        print "---------- Certificate key length -----------"
        conn_logs = 0
        ssl_logs = 0
        x509_logs = 0
        temp_dict = dict()
        for key in self.connection_4_tuples.keys():
            conn_logs += self.connection_4_tuples[key].get_number_of_flows()
            ssl_logs += self.connection_4_tuples[key].get_number_of_ssl_logs()
            x509_logs += self.connection_4_tuples[key].get_size_of_x509_list()
            for a in self.connection_4_tuples[key].get_certificate_key_length_dict().keys():
                try:
                    temp_dict[a] += self.connection_4_tuples[key].get_certificate_key_length_dict()[a]
                except:
                    temp_dict[a] = self.connection_4_tuples[key].get_certificate_key_length_dict()[a]
        print temp_dict
        print "conn_logs", conn_logs
        print "ssl_logs", ssl_logs
        print "x509_logs", x509_logs

    def print_version_of_ssl_dict(self):
        print "---------------------------------------------------------"
        print "---------- Version of ssl dict (serever chose) -----------"
        conn_logs = 0
        ssl_logs = 0
        temp_dict = dict()
        for key in self.connection_4_tuples.keys():
            conn_logs += self.connection_4_tuples[key].get_number_of_flows()
            ssl_logs += self.connection_4_tuples[key].get_number_of_ssl_logs()
            for a in self.connection_4_tuples[key].get_version_of_ssl_dict().keys():
                try:
                    temp_dict[a] += self.connection_4_tuples[key].get_version_of_ssl_dict()[a]
                except:
                    temp_dict[a] = self.connection_4_tuples[key].get_version_of_ssl_dict()[a]
        print temp_dict
        print "conn_logs", conn_logs
        print "ssl_logs", ssl_logs

    def print_certificate_serial(self):
        print "---------------------------------------------------------"
        print "---------- Certificate serial -----------"
        cert_serials = 0

        temp_dict = dict()
        for key in self.connection_4_tuples.keys():
            cert_serials += len(self.connection_4_tuples[key].get_certificate_serial_dict())
            # here is...
            for key2 in self.connection_4_tuples[key].get_certificate_serial_dict():
                try:
                    temp_dict[key2] += 1
                except:
                    temp_dict[key2] = 1
        print "Amout of distinct certificate in their connection object:", cert_serials
        print "Amout of distinct certificate in entire dataset:", len(temp_dict)