"""
python Main_multi.py
This Main is multi, because it processes more single data sets. It means there is a folder where you can find
at least one single datsets. Single dataset is folder where you can find: bro folder, pcap file and binetflow file.
"""

import sys
import ConfigManager
import GetInfectedIPs
from ProcessLogs import ProcessLogs
from PrintManager import __PrintManager__

if __name__ == "__main__":

    __PrintManager__.welcome_main_multi()

    # The argument of this program should be name of the resulting plot data file.
    # If there is no argument, default name for plot data is: 'new_plot_data.txt'
    name_of_result = "new_plot_data.txt"
    if len(sys.argv) == 2:
        name_of_result = sys.argv[1]

    # Get path to multi dataset from config file.
    # [0] - path to single data set
    # [1] - path to multi data set
    path = ConfigManager.read_config()[1]
    if path == -1:
        raise ValueError

    # Get name list of folders which our 'multi folder' contains.
    single_data_sets = ConfigManager.get_folders_in_multi(path)

    __PrintManager__.header_main_multi(path, len(single_data_sets), name_of_result)

    print "<<< Evaluating was started...\n"
    # 2. Create 4-tuples, evaluate features and labeled them.
    process_logs = ProcessLogs(name_of_result)

    for name_single_dir in single_data_sets:
        path_to_single = path + "\\" + name_single_dir
        __PrintManager__.header_of_single_dataset(path_to_single)

        # 1. Get infected IpAddress from labeled binetflow
        # Infected_ips has two components:
        # a. infected_ips[0] = infected_ips_list is array of infected ipAddresses
        # b. infected_ips[1] = infected_ips is dictionary,where index is ipAdrress and value is number of infected ips
        infected_ips = GetInfectedIPs.get_infected_ips(path_to_single)

        # Add infected IPS.
        process_logs.set_infected_ips(infected_ips[0])

        # Process.
        process_logs.evaluate_features(path_to_single)

        __PrintManager__.succ_finished_single_data()

    # Check tuples if each of them has 0 malware or 0 normal.
    process_logs.check_4_tuples()
    # Create plot data for current featues.
    process_logs.create_plot_data()
