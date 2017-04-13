"""
This class stores all information for one "connection 4-tuple" object.
Also it computes features.
"""
import numpy

class Connection4tuple:

    def __init__(self, tuple_index):
        # basic 4-tuple
        self.tuple_index = tuple_index
        # list of flows
        self.ssl_flow_list = []
        self.not_ssl_flow_list = []
        self.x509_list = []
        self.uid_flow_dict = dict()
        self.ssl_logs_list = []
        self.malware_label = 0
        self.normal_label = 0
        self.average_duration_power = 0
        self.flow_which_has_duration_number = 0
        self.duration_list = []

        # Connection Features
        self.number_of_ssl_flows = 0
        self.number_of_not_ssl_flows = 0
        self.number_of_ssl_logs = 0
        self.total_size_of_flows_resp = 0
        self.total_size_of_flows_orig = 0
        self.average_duration = 0
        # Flow features
        self.state_of_connection_dict = dict()
        self.inbound_packtes = 0
        self.outbound_packtes = 0
        # SSL flows
        self.version_of_ssl_dict = dict()
        self.version_of_ssl_cipher_dict = dict()
        self.certificate_path = dict()
        self.ssl_uids_list = []
        # X509 features
        self.certificate_key_type_dict = dict()
        self.certificate_key_length_dict = dict()
        self.certificate_serial_dict = dict()
        self.certificate_valid_length = 0
        self.certificate_valid_length_pow = 0
        self.certificate_valid_number = 0
        self.not_valid_certificate_number = 0
        self.number_san_domains = 0
        self.number_san_domains_index = 0
        self.cert_percent_validity = 0

        self.temp_list = []

        # ssl_flow = this flow has ssl log in ssl file
    def add_ssl_flow(self, flow, label):
        if 'Botnet' in label:
            self.malware_label += 1
        elif 'Normal' in label:
            self.normal_label += 1
        else:
            print "Error in Connectio_4_tuple: Here is label which is not normal or malware (botnet). It is:", label

        # Add this goodonesIPs to the list of goodonesIPs for this 4-tuple.
        self.ssl_flow_list.append(flow)
        self.compute_classic_features(flow)

    # ssl_flow = this flow does not have ssl log in ssl file
    def add_not_ssl_flow(self, flow, label):
        if 'Botnet' in label:
            self.malware_label += 1
        elif 'Normal' in label:
            self.normal_label += 1
        else:
            print "Error in Connectio_4_tuple: Here is label which is not normal or malware (botnet). It is:", label

        self.not_ssl_flow_list.append(flow)
        self.compute_classic_features(flow)

    # ssl_log = ssl line
    # valid_x509_list = x509 lines which were related with this ssl log.
    def add_ssl_log(self, ssl_log, valid_x509_list):
        # compute each x509 line from valid_list (range is 0 or 1)
        for x509_line in range(0, len(valid_x509_list)):
            self.compute_x509_features(valid_x509_list[x509_line])
        # compute ssl log
        self.compute_ssl_features(ssl_log)


    """
    --------- computing methods ---------------
    """
    def compute_classic_features(self, flow):
        # Split the goodonesIPs on elements.
        split = flow.split('	')
        try:
            self.uid_flow_dict[split[1]] += 1
        except:
            self.uid_flow_dict[split[1]] = 1
        # Add state of connection to dict.
        self.add_state_of_connection(split[11])
        # split[9]-orig_bytes, split[10]-resp_bytes
        self.compute_size_of_flow(split[9], split[10])
        # analyze the duration (it can be '-')
        try:
            duration = float(split[8])
            self.process_duration(duration)
        except:
            pass

        # inbound and outbounds packets
        try:
            self.inbound_packtes += int(split[18])
        except:
            print "Error: resp pckts has bad formats."
        try:
            self.outbound_packtes += int(split[16])
        except:
            print "Error: resp pckts has bad formats."

        # perodicity
        # current_time = float(split[0])


    def compute_ssl_features(self, ssl_log):
        self.ssl_logs_list.append(ssl_log)
        split = ssl_log.split('	')
        self.ssl_uids_list.append(split[1])
        try:
            self.version_of_ssl_dict[split[6]] += 1
        except:
            self.version_of_ssl_dict[split[6]] = 1

        try:
            self.version_of_ssl_cipher_dict[split[7]] += 1
        except:
            self.version_of_ssl_cipher_dict[split[7]] = 1

        # Certificate path - number of signed certificate in first certificate
        if split[14] != '-':
            list_of_x509_uids = split[14].split(',')
            try:
                self.certificate_path[len(list_of_x509_uids)] += 1
            except:
                self.certificate_path[len(list_of_x509_uids)] = 1

    def compute_x509_features(self, valid_x509_line):
        self.x509_list.append(valid_x509_line)

        split = valid_x509_line.split('	')

        # certificate_key_type_dict
        try:
            self.certificate_key_type_dict[split[10]] += 1
        except:
            self.certificate_key_type_dict[split[10]] = 1

        # certificate_key_length_dict
        if split[11] != '-':
            try:
                self.certificate_key_length_dict[split[11]] += 1
            except:
                self.certificate_key_length_dict[split[11]] = 1

        # certificate serial number
        try:
            self.certificate_serial_dict[split[3]] += 1
        except:
            self.certificate_serial_dict[split[3]] = 1

        # certificate valid length
        if split[7] != '-' and split[6] != '-':
            try:
                # certificate valid length
                valid_length_sec = float(split[7]) - float(split[6])
                valid_length_days_not_round = int((valid_length_sec / (3600.0 * 24.0)))
                valid_length_days = round(valid_length_days_not_round, 2)
                self.temp_list.append(valid_length_days)

                self.certificate_valid_length += valid_length_days
                self.certificate_valid_length_pow += pow(valid_length_days, 2)
                self.certificate_valid_number += 1

                # check if certificate was valid durig the capture
                current_time = float(split[0])
                before_date = float(split[6])
                after_date = float(split[7])
                if current_time > after_date or current_time < before_date:
                    self.not_valid_certificate_number += 1

                # certificate ratio
                norm_after = after_date - before_date
                current_time_norm = current_time - before_date
                self.cert_percent_validity = current_time_norm / norm_after

            except:
                print "Certificate length is broken."


        # number of domain in san in x509
        if split[14] != '-':
            domains = len(split[14].split(','))
            self.number_san_domains += domains
            self.number_san_domains_index += 1

    "------------------- Methods --------------------------------------"
    """
    orig_bytes - The number of payload bytes the originator sent.
    resp_bytes - The number of payload bytes the responder sent.
    """
    def compute_size_of_flow(self, orig_bytes, resp_bytes):
        try:
            orig_bytes_number = int(orig_bytes)
        except:
            if orig_bytes != '-':
                print "Error: orig_bytes has bad format."
            orig_bytes_number = 0
        try:
            resp_bytes_number = int(resp_bytes)
        except:
            if resp_bytes != '-':
                print "Error: resp_bytes has bad format."
            resp_bytes_number = 0
        self.total_size_of_flows_orig += orig_bytes_number
        self.total_size_of_flows_resp += resp_bytes_number

    """
    Adding state of connetion of this goodonesIPs. Example: "S0", "S1"...
    index meaning
    S0, S1, SF, REJ, S2, S3, RSTO, RSTR, RSTOS0, RSTRH, SH, SHR, OTH,
    """
    def add_state_of_connection(self, state):
        if state not in self.state_of_connection_dict.keys():
            self.state_of_connection_dict[state] = 1
        else:
            self.state_of_connection_dict[state] += 1

    def process_duration(self, duration_value):
        self.flow_which_has_duration_number += 1
        self.duration_list.append(duration_value)
        # 1. EX of duration
        self.average_duration += duration_value
        # 2. EX^2
        self.average_duration_power += pow(duration_value, 2)

    def get_periodicity_list(self):
        final_flow_list = self.ssl_flow_list + self.not_ssl_flow_list
        flows_times_list = []
        for i in range(len(final_flow_list)):
            split = final_flow_list[i].split('	')
            flows_times_list.append(float(split[0]))
        sorted_times_list = sorted(flows_times_list)
        T2_1 = None
        T2_2 = None
        T3 = None
        last_flow = None
        time_diff_list = []
        for i in range(len(sorted_times_list)):
            if last_flow == None:
                last_flow = sorted_times_list[i]
                continue
            if T2_1 == None:
                T2_1 = sorted_times_list[i] - last_flow
                last_flow = sorted_times_list[i]
                continue

            T2_2 = sorted_times_list[i] - last_flow
            T3 = abs(T2_2 - T2_1)
            T2_1 = T2_2
            last_flow = sorted_times_list[i]
            time_diff_list.append(T3)
        return time_diff_list

    """
    ---------- Get Feature -------------------
    """
    # ---------------------------------------------------
    # 01. ---------- Number of flows ------------------
    def get_number_of_flows(self):
        return self.get_number_of_ssl_flows() + self.get_number_of_not_ssl_flows()

    # ---------------------------------------------------
    # ---------- Duration of flows ------------------
    # 02. Average
    def get_average_of_duration(self):
        self.check_zero_dividing(self.flow_which_has_duration_number, "flow_which_has_duration_number is 0 !!!")
        return self.average_duration / float(self.flow_which_has_duration_number)

    # 03. Standard deviation
    def get_standard_deviation_duration(self):
        self.check_zero_dividing(self.flow_which_has_duration_number, "flow_which_has_duration_number is 0 !!!")

        # EX = self.average_duration / float(self.flow_which_has_duration_number)
        # EX2 = self.average_duration_power / float(self.flow_which_has_duration_number) # E(X^2)
        # DX = EX2 - EX*EX
        # return pow(DX, 0.5)
        return numpy.std(self.duration_list)

    # 04. Percent of flows which are bigger or less than standard deviation with average
    def get_percent_of_standard_deviation_duration(self):
        self.check_zero_dividing(self.flow_which_has_duration_number, "flow_which_has_duration_number is 0 !!!")

        out_of_bounds = 0
        lower_level = self.get_average_of_duration() - self.get_standard_deviation_duration()
        upper_level = self.get_average_of_duration() + self.get_standard_deviation_duration()
        for i in range(len(self.duration_list)):
            if self.duration_list[i] < lower_level:
                out_of_bounds += 1
            elif self.duration_list[i] > upper_level:
                out_of_bounds += 1

        return out_of_bounds / float(self.flow_which_has_duration_number)

    # -------------------------------------------------------------------
    # 05 -------- Total payload size of flows the originator sent --------
    def get_total_size_of_flows_orig(self):
        return self.total_size_of_flows_orig

    # ------------------------------------------------------------------
    # 06 -------- Total payload size of flows the responder sent --------
    def get_total_size_of_flows_resp(self):
        return self.total_size_of_flows_resp

    # ---------------------------------------------------------------------------
    # 07 ------ Ratio of responder payload sizes and originator payload sizes ----
    def get_ratio_of_sizes(self):
        # self.check_zero_dividing(self.total_size_of_flows_orig, "Original size is 0 !!!")
        if self.total_size_of_flows_orig != 0:
            return self.total_size_of_flows_resp / float(self.total_size_of_flows_orig)
        return 0

    # --------------------------------------------------------------------
    # ------ State of connection -------------------------------------
    # 08 Percent of established connection
    def get_percent_of_established_states(self):
        establihed_states = 0
        total_value_states = 0
        for key in self.state_of_connection_dict.keys():
            total_value_states += self.state_of_connection_dict[key]
        establihed_states += self.state_of_connection_dict.get('SF', 0)
        establihed_states += self.state_of_connection_dict.get('S1', 0)
        establihed_states += self.state_of_connection_dict.get('S2', 0)
        establihed_states += self.state_of_connection_dict.get('S3', 0)
        establihed_states += self.state_of_connection_dict.get('RSTO', 0)
        establihed_states += self.state_of_connection_dict.get('RSTR', 0)
        return (establihed_states / float(total_value_states))

    # 09 - return 4 items
    def get_based_states_ratio(self):
        SF_S1 = self.state_of_connection_dict['SF'] + self.state_of_connection_dict['S1']
        S0 = self.state_of_connection_dict['S0']
        OTH = self.state_of_connection_dict['OTH']
        REJ = self.state_of_connection_dict['REJ']
        biggest = max(SF_S1, S0, OTH, REJ) / 100.0
        return SF_S1 / float(biggest), S0 / float(biggest), OTH / float(biggest), REJ / float(biggest)

    # 10 - return 6 items
    def get_extended_states_ratio(self):
        SF_S1 = self.state_of_connection_dict['SF'] + self.state_of_connection_dict['S1']
        S0 = self.state_of_connection_dict['S0']
        OTH = self.state_of_connection_dict['OTH']
        REJ = self.state_of_connection_dict['REJ']
        RSTO_1 = self.state_of_connection_dict['RSTO'] + self.state_of_connection_dict['RSTR'] + self.state_of_connection_dict['S2'] + self.state_of_connection_dict['S3']
        RSTO_2 = self.state_of_connection_dict['RSTOS0'] + self.state_of_connection_dict['RSTRH'] + self.state_of_connection_dict['SH'] + self.state_of_connection_dict['SHR']
        biggest = max(SF_S1, S0, OTH, REJ, RSTO_1, RSTO_2) / 100.0
        return SF_S1 / float(biggest), S0 / float(biggest), OTH / float(biggest), REJ / float(biggest), RSTO_1 / float(biggest), RSTO_2 / float(biggest)

    # 11 inbound packets == resp_pkts (18)
    # Number of packets that the responder sent.
    def get_inbound_pckts(self):
        return self.inbound_packtes

    # 12 outbound packets == orig_pkts (16)
    def get_outbound_pckts(self):
        return self.outbound_packtes

    # Periodicity
    # 13 Average of periodicity
    def get_periodicity_average(self):
        per_list = self.get_periodicity_list()
        sum = 0
        for i in range(len(per_list)):
            sum += per_list[i]
        if len(per_list) != 0:
            return sum / float(len(per_list))
        # print "periodicity list is zero. Number of flows:", self.get_number_of_flows()
        return 0

    # 14
    def get_periodicity_standart_deviation(self):
        EX = self.get_periodicity_average()
        per_list = self.get_periodicity_list()
        if len(per_list) != 0:
            # sum = 0
            # for i in range(len(per_list)):
            #     sum += pow(per_list[i], 2)
            # EX2 = sum / float(len(per_list))
            # DX = EX2 - EX * EX
            # return pow(DX, 0.5)
            numpy.std(self.get_periodicity_list())
        return 0

    # -----------------------------------------------------
    # 15 ------ Ratio of not ssl flows and ssl flows -------
    def get_ssl_ratio(self):
        self.check_zero_dividing(len(self.ssl_flow_list), "Original size is 0 !!!")
        return len(self.not_ssl_flow_list) / len(self.ssl_flow_list)

    # 16 Average Public key lenghts
    def get_average_public_key(self):
        total = 0
        index = 0
        for key in self.certificate_key_length_dict.keys():
            total += self.certificate_key_length_dict[key] * int(key)
            index += 1
        if index != 0:
            return total / float(index)
        return 0

    # ------------------------------------------------------
    # 17  Version of ssl ratio
    def get_tls_version_ratio(self):
        tls = 0
        ssl = 0
        total = 0
        for key in self.version_of_ssl_dict.keys():
            if 'TLS' in key:
                tls += self.version_of_ssl_dict[key]
            elif 'SSL' in key:
                ssl += self.version_of_ssl_dict[key]
            total += self.version_of_ssl_dict[key]

        return tls / float(total)

    # ----------------------------------------------
    # Certificate validation length
    # 18 Average of certificate length
    # certificate_valid_length = sum of certificate valid length
    # certificate_valid_number = number of certificate*
    def get_average_of_certificate_length(self):
        # self.check_zero_dividing(self.certificate_valid_number, "certificate_valid_number is 0 !!!")
        if self.certificate_valid_number != 0:
            if numpy.mean(self.temp_list) != self.certificate_valid_length / float(self.certificate_valid_number):
                print "boban"
            return self.certificate_valid_length / float(self.certificate_valid_number)
        return 0

    # 19
    def get_standart_deviation_cert_length(self):
        # self.check_zero_dividing(self.certificate_valid_number, "certificate_valid_number is 0 !!!")
        if self.certificate_valid_number != 0:
            EX = self.certificate_valid_length / self.certificate_valid_number
            EX2 = self.certificate_valid_length_pow / self.certificate_valid_number
            DX = EX2 - (EX * EX)
            # if DX < 0:
            #     print "EX:", (EX*EX)
            #     print "EX2:", EX2
            #     print "DX:", DX
            #     print self.temp_list
            #     print "std:", numpy.std(self.temp_list)
            #     print len(self.x509_list)
            return pow(DX, 0.5)
        return 0

    # ---------------------------------------------
    # 20 Validity of the certificate during the capture
    def is_valid_certificate_during_capture(self):
        return self.not_valid_certificate_number

    # 21 Amount of different certificates
    def get_amount_diff_certificates(self):
        return len(self.certificate_serial_dict.keys())

    # -------------------------------------------------------
    # 22 Number of domains in certificate
    def get_number_of_domains_in_certificate(self):
        if self.number_san_domains_index != 0:
            return self.number_san_domains / float(self.number_san_domains_index)
        return 0

    # 23 Certificate ratio
    def get_certificate_ratio(self):
        return self.cert_percent_validity

    # 24 Certificate path
    # number of signed certificate in our first certificate
    def get_number_of_certificate_path(self):
        up = 0
        down = 0
        for key in self.certificate_path.keys():
            up += int(key) * self.certificate_path[key]
            down += self.certificate_path[key]
        if down != 0:
            return up/float(down)
        return 0

    # 25 x509/ssl ratio
    # ratio about how many ssl log has x509 in this connection
    def x509_ssl_ratio(self):
        return len(self.x509_list) / float(len(self.ssl_logs_list))















    def get_ver_cipher_dict(self):
        return self.version_of_ssl_cipher_dict

    # to histogram
    def get_states_dict(self):
        return self.state_of_connection_dict

    # to histogram
    def get_certificate_key_length_dict(self):
        return self.certificate_key_length_dict

    # to histogram
    def get_version_of_ssl_dict(self):
        return self.version_of_ssl_dict

    # It will be number (number of distinct certificate in connection)
    def get_certificate_serial_dict(self):
        return self.certificate_serial_dict

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

    def get_number_of_ssl_flows(self):
        self.number_of_ssl_flows = len(self.ssl_flow_list)
        return self.number_of_ssl_flows

    def get_number_of_not_ssl_flows(self):
        self.number_of_not_ssl_flows = len(self.not_ssl_flow_list)
        return self.number_of_not_ssl_flows

    def get_uid_flow_dict_length(self):
        return len(self.uid_flow_dict)

    def get_uid_flow_dict(self):
        return self.uid_flow_dict

    def get_number_of_ssl_logs(self):
        self.number_of_ssl_logs = len(self.ssl_logs_list)
        return self.number_of_ssl_logs

    def get_ssl_logs_list(self):
        return self.ssl_logs_list

    def get_malware_label(self):
        return self.malware_label

    def get_normal_label(self):
        return self.normal_label

    def get_size_of_x509_list(self):
        return len(self.x509_list)

    def get_certificate_key_type_dict(self):
        return self.certificate_key_type_dict

    def get_ssl_uids_list(self):
        return self.ssl_uids_list
    """
    Zero exception method
    """
    def check_zero_dividing(self, number, text):
        if number == 0:
            print text
