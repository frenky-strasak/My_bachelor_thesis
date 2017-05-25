"""
https://github.com/frenky-strasak/My_bachelor_thesis
"""
"""
python Main_single.py
This Main is single, because it processes just one data set. It means there is a folder, where zou can find:
bro folder, pcap file and binetflow file.
"""

import sys
import ConfigManager
from ProcessLogs import ProcessLogs
from PrintManager import __PrintManager__

if __name__ == "__main__":

    __PrintManager__.welcome_main_single()

    # The argument of this program should be name of the resulting plot data file.
    # If there is no argument, default name for plot data is: 'new_plot_data.txt'
    name_of_result = "new_plot_data.txt"
    if len(sys.argv) == 2:
        name_of_result = sys.argv[1]

    # Get path to single dataset from config file.
    # [0] - path to single data set
    # [1] - path to multi data set
    path = ConfigManager.read_config()[0]
    if path == -1:
        raise ValueError

    __PrintManager__.header_main_single(path, name_of_result)

    # Create 4-tuples, evaluate features and labeled them.
    process_logs = ProcessLogs(name_of_result)
    # Process.
    process_logs.evaluate_features(path)

    __PrintManager__.set_finish_time()

    # Check tuples if each of them has 0 malware or 0 normal.
    process_logs.check_4_tuples()
    # Create plot data for current featues.
    process_logs.create_plot_data()

    __PrintManager__.succ_main_single()
