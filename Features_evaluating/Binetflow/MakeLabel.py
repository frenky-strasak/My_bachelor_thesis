"""
Usage:
python MakeLabel.py c:\Users\frenk\Documents\Skola\Bachelor_thesis\datasets\Experiment_1
"""
import sys
import glob


# This method returns path with name of the binetflow file.
def find_name_of_binetflow(path_to_folder):
    binetflow_files = glob.glob(path_to_folder + "/*.binetflow")
    if len(binetflow_files) > 1 or len(binetflow_files) == 0:
        return -1
    return binetflow_files[0]


class MakeLabel:
    def __init__(self, path):
        self.path = path
        self.normal_ips = dict()
        self.botnet_ips = dict()
        self.backround_ips = dict()
        self.to_botnet_ips = dict()
        self.to_normal_ips = dict()
        self.flow_array = []

    """
    This function goes to binetflow file and stores ips and their label.
    """
    def process_binetflow(self, entire_path_to_binetflow):
        print "<<< MakeLabel <<<"
        print "<<< Reading binetflow:"
        print "     <<<", entire_path_to_binetflow
        print ""
        count = 0
        normal = 0
        botnet = 0
        to_normal = 0
        to_botnet = 0
        backround = 0
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


                    err = 0
                    if 'From-Botnet' in label:

                        # if index == ('147.32.84.165', '74.125.232.195'):
                        #     print "Hey more ----------------"
                        if split[3] == '147.32.84.165' and split[6] == '74.125.232.195':
                            print "Hey more 0 ----------------"
                            print index
                            if index == ('147.32.84.165', '74.125.232.195'):
                                print "Hey more ----------------"
                        try:
                            self.botnet_ips[index] += 1
                        except:
                            self.botnet_ips[index] = 1
                        err += 1
                        botnet += 1
                    if 'From-Normal' in label:
                        try:
                            self.normal_ips[index] += 1
                        except:
                            self.normal_ips[index] = 1
                        err += 1
                        normal += 1
                    if 'Background' in label:
                        try:
                            self.backround_ips[index] += 1
                        except:
                            self.backround_ips[index] = 1
                        err += 1
                        backround += 1
                    if 'To-Normal' in label:
                        try:
                            self.to_normal_ips[index] += 1
                        except:
                            self.to_normal_ips[index] = 1
                        err += 1
                        to_normal += 1
                    if 'To-Botnet' in label:
                        try:
                            self.to_botnet_ips[index] += 1
                        except:
                            self.to_botnet_ips[index] = 1
                        err += 1
                        to_botnet += 1

                    if err > 1:
                        print "Error in process_binetflow: Label has more labels states!!!"
                        break

                    if err == 0:
                        print "Error in process_binetflow: There is some unknown label."
                        print label
                    count += 1
            f.close()
        except TypeError:
            print "Error: Can not read binetflow file."

        print "     << Number of normal IPs:", normal
        print "     << Length of normal dict:", len(self.normal_ips)
        print "     << Number of botnet IPs:", botnet
        print "     << Length of botnet dict:", len(self.botnet_ips)
        print "     << Number of background IPs:", backround
        print "     << Length of botnet dict:", len(self.backround_ips)
        print "     << Number of lines:", count, ", Together: ", normal + botnet + backround + to_botnet + to_normal

    def read_conn(self,):
            print "<< LabelFile: Reading conn.log and adding labels."

            space = '	'
            index = 0

            normal = 0
            botnet = 0
            to_normal = 0
            to_botnet = 0
            background_count = 0
            zadny = 0
            with open(self.path + '\\bro\\conn.log') as f:
                # go thru file line by line and evaluate each line (line is goodonesIPs)
                for line in f:
                    newline = line
                    if '#' not in line:
                        index += 1
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
                        ips_index = split[2], split[4]



                        err = 0
                        # Botnet flow
                        try:
                            if self.backround_ips[ips_index]:
                                background_count += 1
                                newline = line.rstrip() + space + "Background" + "\n"
                                err += 1
                        except:
                            pass

                        try:
                            if self.normal_ips[ips_index]:
                                normal += 1
                                newline = line.rstrip() + space + "From-Normal" + "\n"
                                err += 1
                        except:
                            pass

                        try:
                            if self.to_normal_ips[ips_index]:
                                to_normal += 1
                                newline = line.rstrip() + space + "To-Normal" + "\n"
                                err += 1
                        except:
                            pass

                        try:
                            if self.botnet_ips[ips_index]:
                                botnet += 1
                                newline = line.rstrip() + space + "From-Botnet" + "\n"
                                err += 1
                        except:
                            pass

                        try:
                            if self.to_botnet_ips[ips_index]:
                                to_botnet += 1
                                newline = line.rstrip() + space + "To-Botnet" + "\n"
                                err += 1
                        except:
                            pass

                        if err == 0:
                            # if split[2] == '147.32.84.165':
                            #     print line
                            #     break
                            zadny += 1
                            newline = line.rstrip() + space + "No_Label" + "\n"

                        if ('147.32.84.165', '74.125.232.195') == ips_index:
                            print "je to tady -------------"
                            print "err:", err
                            print "newline:", newline
                            try:
                                if self.botnet_ips[ips_index]:
                                    print "tento index je v botnet_dict"
                            except:
                                print "tento index neni v botnet_dict"

                        if err > 1:
                            print "<<<< Watch out, more labels for one ips_index. Program was determinate !!!"
                            print line
                            break


                        # # Botnet flow
                        # try:
                        #     if self.backround_ips[ips_index]:
                        #         background_count += 1
                        #         newline = line.rstrip() + space + "Background" + "\n"
                        # except:
                        #     # From-Normal flow
                        #     try:
                        #         if self.normal_ips[ips_index]:
                        #             normal += 1
                        #             newline = line.rstrip() + space + "From-Normal" + "\n"
                        #     except:
                        #         # To-Normal flow
                        #         try:
                        #             if self.to_normal_ips[ips_index]:
                        #                 to_normal += 1
                        #                 newline = line.rstrip() + space + "To-Normal" + "\n"
                        #         except:
                        #             try:
                        #                 if self.botnet_ips[ips_index]:
                        #                     botnet += 1
                        #                     newline = line.rstrip() + space + "From-Botnet" + "\n"
                        #             except:
                        #                 try:
                        #                     if self.to_botnet_ips[ips_index]:
                        #                         to_botnet += 1
                        #                         newline = line.rstrip() + space + "To-Botnet" + "\n"
                        #                 except:
                        #                         zadny += 1
                        #                         newline = line.rstrip() + space + "No_Label" + "\n"
                        #                         # print split[2], split[3], split[4], split[5], split[6]

                    else:
                        if 'fields' in line:
                            newline = line.rstrip() + space + "label" + "\n"
                        elif 'types' in line:
                            newline = line.rstrip() + space + "string" + "\n"

                    self.flow_array.append(newline)

            f.close()

            print "     << These labels were added:"
            print "     << Normal:", normal
            print "     << Botnet:", botnet
            print "     << BackgroundIPs:", background_count
            print "     << No Label", zadny
            print "     << To-Normal", to_normal
            print "     << To-Botnet", to_botnet
            print "     << Together:", background_count + normal + botnet + zadny + to_normal + to_botnet
            print "     << Number of lines:", index

    def write_conn(self):
        print "<< Writing new flows to conn_label.log."
        index = 0
        with open(self.path + '\\bro\\conn_label.log', 'w') as f:
            for i in range(len(self.flow_array)):
                f.write(self.flow_array[i])
                index += 1
        f.close()
        print "     << Number of lines:", index
        print "<< New file conn_label.log was succesfly created."

"""
-----------------------------------------------------------------------------------------------------------------
"""


def check_conn_label(path_to_dataset, infected_ips_list, normal_ips_list):

    print "--------- Checking conn file -------------"

    flow_array = []
    space = '	'
    with open(path_to_dataset + '\\bro\\conn.log') as f:

        for line in f:
            newline = line
            if '#' not in line:
                split = line.split('	')
                src_address = split[2]

                err = 0
                if src_address in infected_ips_list:
                    newline = line.rstrip() + space + "From-Botnet" + "\n"
                    err += 1

                if src_address in normal_ips_list:
                    newline = line.rstrip() + space + "From-Normal" + "\n"
                    err += 1

                if err == 0:
                    newline = line.rstrip() + space + "Background" + "\n"

                if err > 1:
                    print "Error: SrcAddress has more classes. Program is terminated."
                    break
            else:
                if 'fields' in line:
                    newline = line.rstrip() + space + "label" + "\n"
                elif 'types' in line:
                    newline = line.rstrip() + space + "string" + "\n"

            flow_array.append(newline)
    f.close()
    return flow_array


def process_binetflow_2(entire_path_to_binetflow):
        print "<<< MakeLabel <<<"
        print "<<< Reading binetflow:"
        print "     <<<", entire_path_to_binetflow
        print ""

        infected_ips_list = []
        normal_ips_list = []

        try:
            with open(entire_path_to_binetflow) as f:
                for line in f:
                    if 'StartTime' in line:
                        continue
                    split = line.split(',')

                    # split[3] - SrcAddress
                    # split[6] - DstAddress
                    label = split[14]
                    src_address = split[3]

                    if 'From-Botnet' in label:
                        if not(src_address in infected_ips_list):
                            infected_ips_list.append(src_address)

                    elif 'From-Normal' in label:
                        if not(src_address in normal_ips_list):
                            normal_ips_list.append(src_address)
            f.close()
        except TypeError:
            print "Error: Can not read binetflow file."

        print "In our infected ips list is:", infected_ips_list
        print "In our normal ips list is:", normal_ips_list
        return infected_ips_list, normal_ips_list

def write_conn_2(path, flow_array):
    print "<< Writing new flows to conn_label.log."
    index = 0
    with open(path + '\\bro\\conn_label.log', 'w') as f:
        for i in range(len(flow_array)):
            f.write(flow_array[i])
            index += 1
    f.close()
    print "     << Number of lines:", index
    print "<< New file conn_label.log was succesfly created."


if __name__ == '__main__':

    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = None

    path_to_binet = find_name_of_binetflow(path)
    infected_ips_list, normal_ips_list = process_binetflow_2(path_to_binet)
    flow_array = check_conn_label(path, infected_ips_list, normal_ips_list)
    write_conn_2(path, flow_array)


    # For previous version
    # if len(sys.argv) == 2:
    #     path = sys.argv[1]
    # else:
    #     path = None
    #
    # path_to_binet = find_name_of_binetflow(path)
    #
    # label_conn_log = MakeLabel(path)
    # label_conn_log.process_binetflow(path_to_binet)
    # label_conn_log.read_conn()
    # label_conn_log.write_conn()
