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
        self.uid_flow_list = []
        self.ssl_logs_list = []
        self.malware_label = 0
        self.normal_label = 0
        # Features
        self.number_of_flows = 0
        self.number_of_ssl_logs = 0
        self.total_size_of_flows = 0
        self.state_of_connection = dict()

    def add_flow(self, flow, label):
        if label == "MALWARE":
            self.malware_label += 1
        else:
            self.normal_label += 1

        self.compute_classic_features(flow)

    def add_ssl_log(self, ssl_log):
        self.compute_ssl_features(ssl_log)

    def compute_classic_features(self, flow):
        # Split the flow on elements.
        split = flow.split('	')
        # Add this flow to the list of flow for this 4-tuple.
        self.flow_list.append(flow)
        # Add uid of this flow to uid list.
        self.uid_flow_list.append(split[1])
        # Add state of connection to dict.
        self.add_state_of_connection(split[11])

    def compute_ssl_features(self, ssl_log):
        self.ssl_logs_list.append(ssl_log)
        split = ssl_log.split('	')

    """
    Adding state of connetion of this flow. Example: "S0", "S1"...
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

    def get_number_of_flows(self):
        self.number_of_flows = len(self.flow_list)
        return self.number_of_flows

    def get_uid_flow_list(self):
        return self.uid_flow_list

    def get_number_of_ssl_logs(self):
        self.number_of_ssl_logs = len(self.ssl_logs_list)
        return self.number_of_ssl_logs

    def get_malware_label(self):
        return self.malware_label

    def get_normal_label(self):
        return self.normal_label

    def get_states_dict(self):
        return self.state_of_connection

