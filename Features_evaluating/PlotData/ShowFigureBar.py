"""
This file plots a bar figure.
It needs name of data file as first argument.
Example: python ShowFigure2D.py plot_data_1.txt
"""
import sys
import numpy as np
import matplotlib.pyplot as plt

names_of_states = []
malware_states = []
normal_states = []


def read_plot_data_file(name_of_file):
    reading_malware = True
    index_normal = 0
    with open(name_of_file) as f:
            for line in f:
                if '# NORMAL' in line:
                    reading_malware = False
                    continue
                if '#' in line:
                    continue
                split = line.split(': ')
                if reading_malware:
                    names_of_states.append(split[0])
                    malware_states.append(split[1])
                else:
                    if split[0] != names_of_states[index_normal]:
                        print "Error: Sequence of state name is not same for malware and normal!"
                        return False
                    normal_states.append(split[1])
                    index_normal += 1

    f.close()


def create_plot():
    N = len(names_of_states)
    # menMeans = (20, 35, 30, 35, 27)
    # womenMeans = (25, 32, 34, 20, 25)
    # menStd = (2, 3, 4, 1, 2)
    # womenStd = (3, 5, 2, 3, 3)
    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence

    # p1 = plt.bar(ind, menMeans, width, color='r', yerr=menStd)
    # p2 = plt.bar(ind, womenMeans, width, color='y',
    #              bottom=menMeans, yerr=womenStd)

    p1 = plt.bar(ind, malware_states, width, color='r')
    p2 = plt.bar(ind, normal_states, width, color='y',
                 bottom=malware_states)

    plt.ylabel('Number of state')
    plt.title('Number of each type state.')
    plt.xticks(ind + width/2., names_of_states)
    # plt.yticks(np.arange(0, 81, 10))
    plt.legend((p1[0], p2[0]), ('Malware', 'Normal'))

    plt.show()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        name_of_datafile = sys.argv[1]
        read_plot_data_file(name_of_datafile)
        create_plot()
    else:
        print "Error: There must be exactly one argument as name of the data file."


