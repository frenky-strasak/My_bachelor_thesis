class ComputeFeatures:

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
        self.number_of_flows = None
        self.number_of_ssl_logs = None
        self.total_size_of_flows = None

    def add_flow(self, flow, label):
        if label == "MALWARE":
            self.malware_label += 1
        else:
            self.normal_label += 1

        self.compute_classic_features(flow)

    def compute_classic_features(self, flow):
        split = flow.split('	')
        self.flow_list.append(flow)
        # pridani uid daneho flowu do uid_listu
        self.uid_flow_list.append(split[1])



    def add_ssl_log(self, ssl_log):
        self.compute_ssl_features(ssl_log)

    def compute_ssl_features(self, ssl_log):
        self.ssl_logs_list.append(ssl_log)
        split = ssl_log.split('	')

    # GET - METHODS
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

    def print_features(self):
        print "ID 4-tuple: ", self.tuple_index
        print "Number of flows: ", self.number_of_flows
        print "Number of ssl log: ", self.number_of_ssl_logs
        print "Number of MALWARE flows: ", self.malware_label
        print "Number of NORMAL flows: ", self.normal_label
        print "--------------------------------------------------------------"
