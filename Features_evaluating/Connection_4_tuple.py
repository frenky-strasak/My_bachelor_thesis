"""
This class stores all information for one "connection 4-tuple" object.
Also it computes features.
"""


class Connection4tuple:

    def __init__(self, tuple_index):
        # basic 4-tuple
        self.tuple_index = tuple_index
        # list of flows
        self.flow_list = []
        self.uid_flow_dict = dict()
        self.ssl_logs_list = []
        self.malware_label = 0
        self.normal_label = 0

        # Connection Features
        self.number_of_flows = 0
        self.number_of_ssl_logs = 0
        self.total_size_of_flows = 0
        # Flow features
        self.state_of_connection = dict()
        self.version_of_ssl = dict()
        # X509 features
        self.certificate_key_type_dict = dict()
        self.certificate_key_length_dict = dict()
        self.certificate_serial = dict()

    def add_flow(self, flow, label):
        if 'Botnet' in label:
            self.malware_label += 1
        elif 'Normal' in label:
            self.normal_label += 1
        else:
            print "Error in Connectio_4_tuple: Here is label which is not normal or malware (botnet). It is:", label

        self.compute_classic_features(flow)

    def add_ssl_log(self, ssl_log, valid_x509_list):
        # compute each x509 line from valid_list
        for uid in range(0, len(valid_x509_list)):
            self.compute_x509_features(valid_x509_list[uid])
        # compute ssl log
        self.compute_ssl_features(ssl_log)
    """
    --------- computing methods ---------------
    """
    def compute_classic_features(self, flow):
        # Split the goodonesIPs on elements.
        split = flow.split('	')
        # Add this goodonesIPs to the list of goodonesIPs for this 4-tuple.
        self.flow_list.append(flow)
        # Add uid of this goodonesIPs to uid list.
        try:
            self.uid_flow_dict[split[1]] += 1
        except:
            self.uid_flow_dict[split[1]] = 1
        # Add state of connection to dict.
        self.add_state_of_connection(split[11])
        # split[9]-orig_bytes, split[10]-resp_bytes
        self.compute_size_of_flow(split[9], split[10])

    def compute_ssl_features(self, ssl_log):
        self.ssl_logs_list.append(ssl_log)
        split = ssl_log.split('	')
        try:
            self.version_of_ssl[split[6]] += 1
        except:
            self.version_of_ssl[split[6]] = 1

    def compute_x509_features(self, valid_x509_line):
        split = valid_x509_line.split('	')

        # certificate_key_type_dict
        try:
            self.certificate_key_type_dict[split[10]] += 1
        except:
            self.certificate_key_type_dict[split[10]] = 1

        # certificate_key_length_dict
        try:
            self.certificate_key_length_dict[split[11]] += 1
        except:
            self.certificate_key_length_dict[split[11]] = 1

        # certificate serial number
        try:
            self.certificate_serial[split[3]] += 1
        except:
            self.certificate_serial[split[3]] = 1

    def compute_size_of_flow(self, orig_bytes, resp_bytes):
        try:
            orig_bytes_number = int(orig_bytes)
        except:
            orig_bytes_number = 0
        try:
            resp_bytes_number = int(resp_bytes)
        except:
            resp_bytes_number = 0
        self.total_size_of_flows += orig_bytes_number + resp_bytes_number

    """
    Adding state of connetion of this goodonesIPs. Example: "S0", "S1"...
    index meaning
    S0, S1, SF, REJ, S2, S3, RSTO, RSTR, RSTOS0, RSTRH, SH, SHR, OTH,
    """
    def add_state_of_connection(self, state):
        if state not in self.state_of_connection.keys():
            self.state_of_connection[state] = 1
        else:
            self.state_of_connection[state] += 1

    """
    ------------ get methods -----------------
    """
    def get_label_of_connection(self):
        if self.malware_label > self.normal_label:
            return "MALWARE"
        else:
            return "NORMAL"

    def is_malware(self):
        if self.malware_label > self.normal_label:
            return True

    def is_uid_in_dict(self, key):
        label = 0
        try:
            label = self.uid_flow_dict[key]
            return True
        except:
            return False

    def get_number_of_flows(self):
        self.number_of_flows = len(self.flow_list)
        return self.number_of_flows

    def get_uid_flow_dict_length(self):
        return len(self.uid_flow_dict)

    def get_uid_flow_dict(self):
        return self.uid_flow_dict

    def get_number_of_ssl_logs(self):
        self.number_of_ssl_logs = len(self.ssl_logs_list)
        return self.number_of_ssl_logs

    def get_malware_label(self):
        return self.malware_label

    def get_normal_label(self):
        return self.normal_label

    def get_states_dict(self):
        return self.state_of_connection

    def get_total_size_of_flows(self):
        return self.total_size_of_flows

    def get_certificate_key_length_dict(self):
        return self.certificate_key_length_dict

    def get_certificate_key_type_dict(self):
        return self.certificate_key_type_dict

    def get_certificate_serial_dict(self):
        return self.certificate_serial

    def get_version_of_ssl_dict(self):
        return self.version_of_ssl
