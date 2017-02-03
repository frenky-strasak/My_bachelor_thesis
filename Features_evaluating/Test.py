import sys
import time
import datetime

def evaluate_ssl_file(path_to_dataset, x509_dict):
        number_of_adding_x509 = 0
        count_lines = 0
        count_no_x509 = 0
        ssl_uid_dict = dict()

        karel = 0
        bohdana = 0
        ira = 0
        try:
            with open(path_to_dataset + "\\bro\\ssl.log") as f:
                # go thru ssl file line by line and for each ssl line check all uid of flows
                for line in f:
                    if '#' in line:
                        continue
                    split = line.split('	')
                    ssl_uid = split[1]


                    # print list_of[0]
                    try:
                        line = ssl_uid_dict[ssl_uid]
                        print "Error: SSL more uids!!!", ssl_uid
                    except:
                        ssl_uid_dict[ssl_uid] = line

                    # list_of = split[14].split(',')
                    #
                    # for i in range(len(list_of)):
                    #     if split[14] == '-' or '(object)' == split[14]:
                    #         count_no_x509 += 1
                    #         continue
                    #     try:
                    #         x509_line = x509_dict[list_of[i]]
                    #         if len(x509_dict[list_of[i]]) > 1:
                    #             bohdana += 1
                    #         number_of_adding_x509 += 1
                    #     except:
                    #         print "Error: x509 filu chybi line stimhle keyem:", list_of[i]

                    count_lines += 1
            f.close()

            print "evaluate_ssl_file: Pocet radku:", count_lines
            print "evaluate_ssl_file: Velikost dict:", len(ssl_uid_dict)
            # print "evaluate_ssl_file: number_of_adding_x509:", number_of_adding_x509
            # print "evaluate_ssl_file: flows bez x509:", count_no_x509

            # print "karel - :", karel
            print "SSL logs needs tolik x509 s vice stejnymi uids :", bohdana
            # print "ira [] :", ira
            # print "Dohromady: x :", bohdana + karel + ira

        except IOError:
           print "prdlacky"
        return ssl_uid_dict


def evaluate_x509(path_to_dataset):
        number_adding_ssl = 0
        count_lines = 0
        ssl_uid_dict = dict()
        cert_key_type = dict()
        try:
            with open(path_to_dataset + "\\bro\\x509.log") as f:
                # go thru ssl file line by line and for each ssl line check all uid of flows
                for line in f:
                    if '#' in line:
                        continue
                    split = line.split('	')
                    ssl_uid = split[1]

                    try:
                        ssl_uid_dict[ssl_uid].append(line)
                        print "Error: x509 more uids!!!", ssl_uid
                    except:
                        ssl_uid_dict[ssl_uid] = []
                        ssl_uid_dict[ssl_uid].append(line)

                    try:
                        cert_key_type[split[11]] += 1
                    except:
                        cert_key_type[split[11]] = 1

                    count_lines += 1
            f.close()

            print "evaluate_x509: Pocet radku:", count_lines
            print "evaluate_x509: Velikost dict:", len(ssl_uid_dict)
        except IOError:
           print "prdlacky"
        return ssl_uid_dict
        # return cert_key_type

def read_conn(path, ssl_uid_dict, x509_uids):
        connection_4_tuple = dict()
        space = '	'
        index = 0

        with open(path + '\\bro\\conn_label.log') as f:
            # go thru file line by line and evaluate each line (line is goodonesIPs)
            # 1496
            hitrate = 0
            anti_hitrate = 0
            number_of_adding_x509_malware = 0
            number_of_adding_x509_normal = 0

            number_of_adding_ssl_malware = 0
            number_of_adding_ssl_normal = 0

            malware_cert_diff = []
            normal_cert_diff = []

            for line in f:

                newline = line
                if '#' not in line:
                    split = line.split('	')
                    connection_index = split[2], split[4], split[5], split[6]
                    con_uid = split[1]
                    label = split[21]

                    try:
                        ssl_line = ssl_uid_dict[con_uid]
                        anti_hitrate += 1
                        if 'Botnet' in label or 'Normal' in label:
                            if 'Botnet' in label:
                                number_of_adding_ssl_malware += 1
                            elif 'Normal' in label:
                                number_of_adding_ssl_normal += 1
                            hitrate += 1
                            ssl_split = ssl_line.split('	')
                            split = ssl_split[14].split(',')
                            for i in range(len(split)):
                                if ssl_split[14] == '-' or '(object)' == ssl_split[14]:
                                    continue
                                try:
                                    x509_list = x509_uids[split[i]]


                                    if len(x509_list) > 1:
                                        print "Error: Ma to delku vetsi nez 1."

                                    x509_line = x509_list[0]
                                    # print x509_line
                                    x_509_split = x509_line.split('	')

                                    certificate_not_valid_before = x_509_split[6]
                                    certificate_not_valid_after = x_509_split[7]

                                    try:
                                        # print "string:", certificate_not_valid_after
                                        # print "int:", float(certificate_not_valid_after)
                                        time_diff = float(certificate_not_valid_after) - float(certificate_not_valid_before)
                                    except:
                                        print "aplpl"
                                    # time_diff = 0


                                    v1 = datetime.datetime.fromtimestamp(float(certificate_not_valid_before)).strftime('%Y-%m-%d %H:%M:%S')
                                    v2 = datetime.datetime.fromtimestamp(float(certificate_not_valid_after)).strftime('%Y-%m-%d %H:%M:%S')
                                    diff = ((float(certificate_not_valid_after) - float(certificate_not_valid_before) ) /3600.0 ) / 24.0
                                    if 'Botnet' in label:
                                        number_of_adding_x509_malware += 1
                                        # malware_cert_diff.append(time_diff)
                                        text = "Malware : before:",v1, "after: ", v2, "diff", diff
                                        malware_cert_diff.append(text)
                                    elif 'Normal' in label:
                                        number_of_adding_x509_normal += 1
                                        # normal_cert_diff.append(time_diff)
                                        text = "Normal : before:",v1, "after: ", v2, "diff", diff
                                        normal_cert_diff.append(text)

                                    else:
                                        print "Error : Je to spatne.."
                                except:
                                    print "Error: x509 filu chybi line stimhle keyem:", split[i]
                        else:
                            pass
                    except:
                        pass

                    index += 1

        f.close()

        print "file:", index
        print "hitrate :", hitrate
        print "antihitrate :", anti_hitrate
        print "number_of_adding_x509_malware :", number_of_adding_x509_malware
        print "number_of_adding_x509_normal :", number_of_adding_x509_normal

        print "number_of_adding_ssl_malware :", number_of_adding_ssl_malware
        print "number_of_adding_ssl_normal :", number_of_adding_ssl_normal

        # print normal time diff
        print "Normal time certificate diff"
        for i in range(0, len(normal_cert_diff)):
            print normal_cert_diff[i]

        # print malware time diff
        print "Malware time certificate diff"
        for i in range(0, len(malware_cert_diff)):
            print malware_cert_diff[i]



if __name__ == '__main__':
    # if len(sys.argv) == 2:
    #     path = sys.argv[1]
    # else:
    #     path = None
    # dict_uid = evaluate_ssl_file(path)
    # read_conn(path, dict_uid)

    if len(sys.argv) == 2:
        path = sys.argv[1]

        dict_x = evaluate_x509(path)
        ssl_dict = evaluate_ssl_file(path, dict_x)
        read_conn(path, ssl_dict, dict_x)

    # ts_epoch = 1362301382
    # ts = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d %H:%M:%S')
    # print ts

    # a = 1244486607.000000
    # b = 1084399200.000000
    #
    # print a-b

#
# class Base(object):
#     def __init__(self):
#         self.name = None
#         self.value = None
#
#     def get_name(self):
#         return self.name
#
#     def smrdis(self):
#         print "je to: ", self.name
#
#     def get_value(self):
#         print self.value
#
#
# class Derivate(Base):
#     def __init__(self, n1, n2, value):
#         super(Derivate, self).__init__()
#         self.n1 = n1
#         self.n2 = n2
#         self.value = value
#
#     def set_name(self):
#         self.name = "ahoj svete"
#
#     def get_name(self):
#         return self.name
#
#
# if __name__ == "__main__":
#     temp = Derivate(1,2,5)
#     temp.set_name()
#     print temp.get_name()
#     temp.smrdis()
#     temp.get_value()
