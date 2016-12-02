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

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig,  ax = plt.subplots()
    rects1 = ax.bar(ind, malware_states, width, color='r')
    rects2 = ax.bar(ind + width, normal_states, width, color='y')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Number of states')
    ax.set_title('Numbers of connection states')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(names_of_states)
    # For viewing the chart.
    # ax.axis([0,5, 0, 40])
    ax.legend((rects1[0], rects2[0]), ('Malware', 'Normal'))

    def auto_label(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    auto_label(rects1)
    auto_label(rects2)

    # Just for maximizing window.
    # If you get errors just because of it, delete it.
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.show()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        name_of_datafile = sys.argv[1]
        read_plot_data_file(name_of_datafile)
        create_plot()
    else:
        print "Error: There must be exactly one argument as name of the data file."


