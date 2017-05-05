"""
IPs are given as array in argument
Usage:
python LabelFromBinet.py c:\Users\frenk\Documents\Skola\Bachelor_thesis\datasets\Experiment_1 10.0.0.1
"""

import sys
import MakeLabel

if __name__ == '__main__':
    if len(sys.argv) > 2:
        path = sys.argv[1]

        infected_ips = []
        normal_ips = []

        arguments = sys.argv

        # for i in range(2, len(arguments)):
        #     infected_ips.append(arguments[i])


        for i in range(2, len(arguments)):
            normal_ips.append(arguments[i])



        print "infected ips:", infected_ips
        print "normal ips:", normal_ips
        MakeLabel.ips_from_array(path, infected_ips, normal_ips)

    else:
        print "Error: Wrong arguments."