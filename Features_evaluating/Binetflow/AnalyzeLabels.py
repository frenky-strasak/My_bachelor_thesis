"""
1. "process_binetflow" function goes into binetflow file and creates "normal_and_botnet_ips" and "backround_ips" dicionary.
2. "get_binetflow_labels()" function goes also into binetflow file. This function checks if each same 5-tuple has same label.
    Also it stores 5-tuples and their labels.
3. "read_conn()" function goes into conn.log. It takes flow from conn.log and looks for in labels dictionary. It prints
statistic.
"""
import glob
import sys


# This method returns path with name of the binetflow file.
def find_name_of_binetflow(path_to_folder):
    binetflow_files = glob.glob(path_to_folder + "/*.binetflow")
    if len(binetflow_files) > 1 or len(binetflow_files) == 0:
        return -1
    return binetflow_files[0]


def process_binetflow(entire_path_to_binetflow):
    count = 0
    normal_and_botnet_ips = dict()
    backround_ips = dict()
    try:
        with open(entire_path_to_binetflow) as f:
            for line in f:
                if 'StartTime' in line:
                    continue
                split = line.split(',')

                # split[3] - SrcAddress
                # split[6] - DstAddress
                index = split[3], split[6]
                label = split[14]

                if 'Botnet' in label or 'Normal' in label:
                    try:
                        normal_and_botnet_ips[index] += 1
                    except:
                        normal_and_botnet_ips[index] = 1
                else:
                    try:
                        backround_ips[index] += 1
                    except:
                        backround_ips[index] = 1
                count += 1
        f.close()
    except TypeError:
        print "Error more."

    print "process_binetflow:"
    print "     pocet ok: ", len(normal_and_botnet_ips)
    print "     pocet back: ", len(backround_ips)
    print "     dohromady: ", (len(backround_ips) + len(normal_and_botnet_ips))
    print "     pocet flows: ", count

    print "     -----"
    good = 0
    for key in normal_and_botnet_ips.keys():
        good += normal_and_botnet_ips[key]
    print "     Pocet Goodones:", good
    bad = 0
    for key in backround_ips.keys():
        bad += backround_ips[key]
    print "     Pocet backgrounds:", bad
    print "     Dohromady:", bad + good

    return normal_and_botnet_ips, backround_ips


class LabelFile:
    def __init__(self, path):
        self.flows = dict()
        self.flow_array = []
        self.path = path

    def get_binetflow_labels(self, path_to_binet):
        print "LabelFile: Getting labels from binetflow file."

        index = 0
        temp = 0

        try:
            with open(path_to_binet) as f:
                for line in f:
                    if 'StartTime' in line:
                        continue
                    split = line.split(',')

                    # split[3] - SrcIP
                    # split[4] - SrcPort
                    # split[6] - DstIP
                    # split[7] - DstPort
                    # split[2] - Protocol
                    key = split[3], split[4], split[6], split[7], split[2]
                    label = split[14]

                    # Fast way
                    try:
                        new_label = self.flows[key]
                        temp_label, err = get_label(label)
                        if new_label != temp_label:
                            print "Error: Flows have more kinds of labels. ------------------------"
                            print line
                            # print label
                            break
                        temp += 1
                    except:
                        temp_label, err = get_label(label)
                        if err > 1:
                            print "Error: Bad label!!! ----------------------"
                            break
                        self.flows[key] = temp_label

                    if index % 40000 == 0:
                        # print index
                        pass

                    index += 1
            f.close()
            print "     Velikost dict:", len(self.flows)
            print "     Pocet stejnych 5-tuple:", temp
            print "     Pocet flows celkem:", len(self.flows) + temp

        except TypeError:
            print "Error: Can not read file."

    def read_conn(self, flow_ips, backgroundIPs):
        print "LabelFile: Reading conn.log and adding labels."

        space = '	'
        index = 0
        error = 0

        normal_key = 0
        crazy_key = 0
        goodIps_count = 0
        background_count = 0
        zadny = 0
        with open(self.path + '\\bro\\conn.log') as f:
            # go thru file line by line and evaluate each line (line is goodonesIPs)
            for line in f:

                newline = line
                if '#' not in line:
                    split = line.split('	')
                    # Binetflow:
                    # split[3] - SrcIP
                    # split[4] - SrcPort
                    # split[6] - DstIP
                    # split[7] - DstPort
                    # split[2] - Protocol
                    # Bro:
                    # split[2] - srcIP,
                    # split[3] - SrcPort,
                    # split[4] - DstIP
                    # split[5] - DstPort
                    # split[6] - Protocol
                    key = split[2], split[3], split[4], split[5], split[6]
                    key2 = split[4], split[5], split[2], split[3], split[6]
                    ips_index = split[2], split[4],
                    ips_index2 = split[4], split[2],
                    try:
                        label = self.flows[key]
                        # print "     Right, This key is there:", key
                        newline = line.rstrip() + space + label + "\n"
                        normal_key += 1
                    except:
                        try:
                            label = self.flows[key2]
                            # print "     Right, This key is there:", key
                            newline = line.rstrip() + space + label + "\n"
                            crazy_key += 1
                        except:
                            # print "Error: There is no this key:", key2
                            error = -1
                            try:
                                if flow_ips[ips_index]:
                                    goodIps_count += 1
                            except:
                                try:
                                    if flow_ips[ips_index2]:
                                        goodIps_count += 1
                                except:
                                    try:
                                        if backgroundIPs[ips_index]:
                                            background_count += 1
                                    except:
                                        try:
                                            if backgroundIPs[ips_index2]:
                                                background_count += 1
                                        except:
                                            zadny += 1
                                            print "prazdna ip:", split[2], split[3], split[4], split[5], split[6]
                    index += 1
                else:
                    if 'fields' in line:
                        newline = line.rstrip() + space + "label" + "\n"
                    elif 'types' in line:
                        newline = line.rstrip() + space + "string" + "\n"

                self.flow_array.append(newline)
        f.close()
        print "     normalkeys:", normal_key
        print "     crazykeys:", crazy_key
        print "     Goodones:", goodIps_count
        print "     Backgrounds:", background_count
        print "     Zadny:", zadny
        print "     Dohromady:", background_count + goodIps_count + zadny + normal_key + crazy_key
        print "     Number of lines:", index

        return error


def get_label(label):
        temp = 0
        name = None
        if 'Normal' in label:
            temp += 1
            name = 'Normal'
        if 'Botnet' in label:
            temp += 1
            name = 'Botnet'
        if 'Background' in label:
            temp += 1
            name = 'Background'
        if temp == 0:
            temp = 10

        return name, temp

"""
This function checks if some ip has somewhere botnetlabel so if it has this label every time
"""
def chack_botnet_ips(path_to_binet):

    infected_ips_dict = dict()
    normal_ips_dict = dict()
    normal_err = 0
    malware_err = 0

    with open(path_to_binet) as f:
        for line in f:
            if 'StartTime' in line:
                continue
            split = line.split(',')

            # split[3] - SrcIP
            # split[4] - SrcPort
            # split[6] - DstIP
            # split[7] - DstPort
            # split[2] - Protocol
            src_ip = split[3]
            label = split[14]

            # Test malware
            try:
                if infected_ips_dict[src_ip]:
                    if 'From-Botnet' in label:
                        infected_ips_dict[src_ip] += 1
                    else:
                        malware_err += 1
            except:
                if 'From-Botnet' in label:
                    infected_ips_dict[src_ip] = 1

            # test normal
            try:
                if normal_ips_dict[src_ip]:
                    if 'From-Normal' in label:
                        normal_ips_dict[src_ip] += 1
                    else:
                        normal_err += 1
            except:
                if 'From-Normal' in label:
                    normal_ips_dict[src_ip] = 1

    f.close()

    print "Normal errors: ", normal_err
    print "Malware errors: ", malware_err
    print infected_ips_dict
    print normal_ips_dict
    return infected_ips_dict, normal_ips_dict


def check_conn_label(path, infected_ips_dict, normal_ips_dict):
    with open(path + '\\bro\\conn_label.log') as f:

        err = 0


        for line in f:
            if '#' not in line:
                split = line.split('	')
                src_address = split[2]
                label = split[21]
                access = 0

                if 'From-Botnet' in label:
                    if src_address in infected_ips_dict.keys():
                        access += 1
                    else:
                        err += 1
                if 'From-Normal' in label:
                    if src_address in normal_ips_dict.keys():
                        access += 1
                    else:
                        err += 1

                if src_address in infected_ips_dict.keys():
                    if 'From-Botnet' in label:
                        access += 1
                    else:
                        err += 1

                if src_address in normal_ips_dict.keys():
                    if 'From-Normal' in label:
                        access += 1
                    else:
                        err += 1

                if access == 0:
                    if "Background" in label:
                        pass
                    else:
                        print "Error: more!!!"

                if access != 0 and access != 2:
                    print "Error: more2!!!"
    f.close()
    print "conn errors:", err

if __name__ == '__main__':

    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = None

    path_to_binet = find_name_of_binetflow(path)

    infected_ips_dict, normal_ips_dict = chack_botnet_ips(path_to_binet)

    check_conn_label(path, infected_ips_dict, normal_ips_dict)
    # Previous verison. Closed 22.03. 2017
    # path_to_binet = find_name_of_binetflow(path)
    #
    # # Finds all infected and normal ips
    # goodonesIPs, backgroundIPs = process_binetflow(path_to_binet)
    # make_label_file = LabelFile(path)
    # # Get label from binet goodonesIPs.
    # make_label_file.get_binetflow_labels(path_to_binet)
    # # Go to bro file, read flows and add label state.
    # if make_label_file.read_conn(goodonesIPs, backgroundIPs) == 0:
    #     # If no error, write flows with labels to new file "conn_label.log"
    #     #make_label_file.write_conn()
    #     pass





"""
Result about right labels in binetflow file. It menas if some Src ip address has label Malware so if every time has malware label.
"""
# c:\Users\frenk\Documents\Skola\Bachelor_thesis\My_bachelor_thesis\Features_evaluating\Binetflow>python AnalyzeLabels.py c:\Users\frenk\Documents\Skola\Bachelor_thesis\datasets\Experiment_1\
# Normal errors:  19
# Malware errors:  0
# {'147.32.84.165': 40961}
# {'147.32.80.9': 83, '147.32.84.134': 3808, '147.32.87.11': 6, '147.32.84.170': 18438, '147.32.87.36': 269, '147.32.84.164': 7654}

# c:\Users\frenk\Documents\Skola\Bachelor_thesis\My_bachelor_thesis\Features_evaluating\Binetflow>python AnalyzeLabels.py c:\Users\frenk\Documents\Skola\Bachelor_thesis\datasets\Experiment_2\
# Normal errors:  12
# Malware errors:  0
# {'147.32.84.165': 20941}
# {'147.32.87.36': 71, '147.32.80.9': 23, '147.32.84.170': 8960, '147.32.87.11': 3, '147.32.84.164': 25}
#
# c:\Users\frenk\Documents\Skola\Bachelor_thesis\My_bachelor_thesis\Features_evaluating\Binetflow>python AnalyzeLabels.py c:\Users\frenk\Documents\Skola\Bachelor_thesis\datasets\Experiment_3\
# Normal errors:  177
# Malware errors:  2
# {'38.229.70.20': 63, '147.32.84.165': 26759}
# {'147.32.80.9': 14, '147.32.84.134': 967, '147.32.87.11': 92, '147.32.84.170': 108807, '147.32.87.36': 1843, '147.32.84.164': 4580}
#
# c:\Users\frenk\Documents\Skola\Bachelor_thesis\My_bachelor_thesis\Features_evaluating\Binetflow>python AnalyzeLabels.py c:\Users\frenk\Documents\Skola\Bachelor_thesis\datasets\Experiment_4\
# Normal errors:  12
# Malware errors:  0
# {'147.32.84.165': 2580}
# {'147.32.80.9': 13, '147.32.84.134': 10482, '147.32.87.11': 4, '147.32.84.170': 12133, '147.32.87.36': 89, '147.32.84.164': 2474}
#
# c:\Users\frenk\Documents\Skola\Bachelor_thesis\My_bachelor_thesis\Features_evaluating\Binetflow>python AnalyzeLabels.py c:\Users\frenk\Documents\Skola\Bachelor_thesis\datasets\Experiment_5\
# Normal errors:  3
# Malware errors:  0
# {'147.32.84.165': 901}
# {'147.32.80.9': 5, '147.32.84.134': 1107, '147.32.87.11': 2, '147.32.84.170': 1810, '147.32.87.36': 14, '147.32.84.164': 1722}
#
# c:\Users\frenk\Documents\Skola\Bachelor_thesis\My_bachelor_thesis\Features_evaluating\Binetflow>python AnalyzeLabels.py c:\Users\frenk\Documents\Skola\Bachelor_thesis\datasets\Experiment_6\
# Normal errors:  7
# Malware errors:  0
# {'147.32.84.165': 4630}
# {'147.32.80.9': 20, '147.32.84.134': 682, '147.32.87.11': 2, '147.32.84.170': 5488, '147.32.87.36': 34, '147.32.84.164': 1245}
#
# c:\Users\frenk\Documents\Skola\Bachelor_thesis\My_bachelor_thesis\Features_evaluating\Binetflow>python AnalyzeLabels.py c:\Users\frenk\Documents\Skola\Bachelor_thesis\datasets\Experiment_7\
# Normal errors:  4
# Malware errors:  0
# {'147.32.84.165': 63}
# {'147.32.87.36': 49, '147.32.84.134': 292, '147.32.80.9': 1, '147.32.84.170': 807, '147.32.84.164': 520}
#
# c:\Users\frenk\Documents\Skola\Bachelor_thesis\My_bachelor_thesis\Features_evaluating\Binetflow>python AnalyzeLabels.py c:\Users\frenk\Documents\Skola\Bachelor_thesis\datasets\Experiment_8\
# Normal errors:  54
# Malware errors:  0
# {'147.32.84.165': 6128}
# {'147.32.80.9': 44, '147.32.84.134': 5463, '147.32.87.11': 19, '147.32.84.164': 18164, '147.32.84.170': 48588, '147.32.87.36': 359, '147.32.1.20': 2}
#
# c:\Users\frenk\Documents\Skola\Bachelor_thesis\My_bachelor_thesis\Features_evaluating\Binetflow>python AnalyzeLabels.py c:\Users\frenk\Documents\Skola\Bachelor_thesis\datasets\Experiment_9\
# Normal errors:  20
# Malware errors:  7
# {'147.32.84.192': 20305, '147.32.84.193': 17961, '147.32.84.191': 18774, '147.32.84.165': 22792, '147.32.84.206': 18553, '147.32.84.207': 16000, '147.32.84.204': 18783, '147.32.84.205': 17535, '147.32.84.208': 17909, '147.32.84.209': 16377}
# {'147.32.80.9': 116, '147.32.84.134': 9419, '147.32.87.11': 6, '147.32.1.20': 3, '147.32.84.170': 15806, '147.32.87.36': 111, '147.32.84.164': 4432}
#
# c:\Users\frenk\Documents\Skola\Bachelor_thesis\My_bachelor_thesis\Features_evaluating\Binetflow>python AnalyzeLabels.py c:\Users\frenk\Documents\Skola\Bachelor_thesis\datasets\Experiment_10\
# Normal errors:  25
# Malware errors:  13
# {'147.32.84.192': 10397, '147.32.84.193': 10009, '147.32.84.191': 10454, '147.32.84.165': 9579, '147.32.84.206': 11287, '147.32.84.207': 10581, '147.32.84.204': 11159, '147.32.84.205': 11874, '147.32.84.208': 11118, '147.32.84.209': 9894}
# {'147.32.80.9': 651, '147.32.84.134': 1091, '147.32.87.11': 4, '147.32.1.20': 16, '147.32.84.170': 10216, '147.32.87.36': 99, '147.32.84.164': 3728}
#
# c:\Users\frenk\Documents\Skola\Bachelor_thesis\My_bachelor_thesis\Features_evaluating\Binetflow>python AnalyzeLabels.py c:\Users\frenk\Documents\Skola\Bachelor_thesis\datasets\Experiment_11\
# Normal errors:  3
# Malware errors:  0
# {'147.32.84.192': 7, '147.32.84.191': 4006, '147.32.84.165': 4151}
# {'147.32.80.9': 1, '147.32.84.134': 11, '147.32.87.11': 2, '147.32.84.170': 581, '147.32.87.36': 1, '147.32.84.164': 2113}
#
# c:\Users\frenk\Documents\Skola\Bachelor_thesis\My_bachelor_thesis\Features_evaluating\Binetflow>python AnalyzeLabels.py c:\Users\frenk\Documents\Skola\Bachelor_thesis\datasets\Experiment_12\
# Normal errors:  5
# Malware errors:  0
# {'147.32.84.192': 570, '147.32.84.191': 766, '69.104.66.134': 4, '222.160.227.154': 5, '93.103.254.175': 4, '91.188.37.153': 4, '147.32.84.165': 807, '161.200.133.204': 4, '95.65.17.47': 4}
# {'147.32.80.9': 3, '147.32.84.134': 2145, '147.32.87.11': 1, '147.32.84.170': 4359, '147.32.87.36': 32, '147.32.84.164': 1075}
#
# c:\Users\frenk\Documents\Skola\Bachelor_thesis\My_bachelor_thesis\Features_evaluating\Binetflow>python AnalyzeLabels.py c:\Users\frenk\Documents\Skola\Bachelor_thesis\datasets\Experiment_13\
# Normal errors:  41
# Malware errors:  0
# {'147.32.84.165': 40003}
# {'147.32.80.9': 6, '147.32.84.134': 948, '147.32.87.11': 18, '147.32.84.170': 26846, '147.32.87.36': 422, '147.32.84.164': 3539}