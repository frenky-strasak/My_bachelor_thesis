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


if __name__ == '__main__':

    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = None

    path_to_binet = find_name_of_binetflow(path)

    # Finds all infected and normal ips
    goodonesIPs, backgroundIPs = process_binetflow(path_to_binet)
    make_label_file = LabelFile(path)
    # Get label from binet goodonesIPs.
    make_label_file.get_binetflow_labels(path_to_binet)
    # Go to bro file, read flows and add label state.
    if make_label_file.read_conn(goodonesIPs, backgroundIPs) == 0:
        # If no error, write flows with labels to new file "conn_label.log"
        #make_label_file.write_conn()
        pass
