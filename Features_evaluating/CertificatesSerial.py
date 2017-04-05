
class CertificateSerial:

    def __init__(self, cert_cerial, x509_uid):
        self.server_name_dict = dict()
        self.server_name_list = []
        self.cert_serial = cert_cerial
        # self.ssl_uid = ssl_uid
        self.x509_uid = x509_uid
        self.tuple_index_list = []

    def add_server_name(self, x509_uids, server_name, ssl_uid, tuple_index):
        if not(server_name in self.server_name_list):
            self.server_name_list.append(server_name)

        try:
            self.server_name_dict[tuple_index].append([x509_uids, server_name, ssl_uid])
        except:
            self.server_name_dict[tuple_index] = []
            self.server_name_dict[tuple_index].append([x509_uids, server_name, ssl_uid])
        if not(tuple_index in self.tuple_index_list):
            self.tuple_index_list.append(tuple_index)

    def is_server_in_list(self, server_name):
        if server_name in self.server_name_list:
            return True
        return False

    def get_server_names_dict(self):
        return self.server_name_dict

    def get_size_servers_list(self):
        return len(self.server_name_dict.keys())

    def get_tuple_index_list(self):
        return self.tuple_index_list