"""
This file goes to binetflow file, where you can find labels for each flow. It gives you all infected ip addresses.
"""
import sys
import glob
from PrintManager import __PrintManager__


def get_infected_ips(path_to_folder):
    __PrintManager__.getinfectedips_getting()
    all_path_to_binetflow = find_name_of_binetflow(path_to_folder)
    (infected_ips_list, infected_ips_dict) = process_binetflow(all_path_to_binetflow)
    return infected_ips_list, infected_ips_dict


# This method returns path with name of the binetflow file.
def find_name_of_binetflow(path_to_folder):
    binetflow_files = glob.glob(path_to_folder + "/*.binetflow")
    if len(binetflow_files) > 1 or len(binetflow_files) == 0:
        return -1
    return binetflow_files[0]


def process_binetflow(entire_path_to_binetflow):
    infected_ips = dict()
    infected_ips_list = []
    normal_ips = dict()
    normal_ips_list = []
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
                if 'Botnet' in label:
                    if index in infected_ips.keys():
                        infected_ips[index] += 1
                    else:
                        infected_ips[index] = 1
                        infected_ips_list.append(index)
                elif 'Normal' in label:
                    if index in normal_ips.keys():
                        normal_ips[index] += 1
                    else:
                        normal_ips[index] = 1
                        normal_ips_list.append(index)
        f.close()
    except TypeError:
        __PrintManager__.getinfectedips_error1()

    return infected_ips_list, infected_ips


# 1. argument is path to folder, where the binetflow is.
# 2. argument is a name of the binetflow
if __name__ == "__main__":
    if len(sys.argv) == 2:
        path_To_Folder = sys.argv[1]
        dict_ips = get_infected_ips(path_To_Folder)

        for key in dict_ips[1].keys():
            print key, dict_ips[1][key]

        print dict_ips[0]

    else:
        __PrintManager__.getinfectedips_error2()
