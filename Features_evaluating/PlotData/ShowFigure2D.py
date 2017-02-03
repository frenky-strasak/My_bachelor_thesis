"""
This file plots a points figure.
It needs name of data file as first argument.
Example: python ShowFigure2D.py plot_data_1.txt
"""
import sys
import matplotlib.pyplot as plt

x_malware = []
y_malware = []

x_normal = []
y_normal = []


def read_plot_data_file(name_of_file):
    number_malware = 0
    number_normal = 0
    title = ''
    x_axis = ''
    y_axis = ''

    with open(name_of_file) as f:
            for line in f:
                if '#' in line:
                    if 'title' in line:
                        title = line.replace('# title: ', '')
                    elif 'x axis' in line:
                        x_axis = line.replace('# x axis: ', '')
                    elif 'y axis' in line:
                        y_axis = line.replace('# y axis: ', '')
                    continue
                split = line.split('<<<')
                if split[1] == "MALWARE":
                    x_malware.append(split[2])
                    y_malware.append(split[3])
                    number_malware += 1
                else:
                    x_normal.append(split[2])
                    y_normal.append(split[3])
                    number_normal += 1
    f.close()
    return number_malware, number_normal, title, x_axis, y_axis


def create_plot(title, x_axis, y_axis):
    # plt.plot([1,2,3,4], [1,4,9,16], 'ro')
    # plt.plot([1,2,3,4], [2,5,10,17], 'bo')

    malware = plt.plot(x_malware, y_malware, 'r^')
    normal = plt.plot(x_normal, y_normal, 'bs')

    # plt.axis([0, 6, 0, 20])
    plt.grid(True)
    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.legend((malware[0], normal[0]), ('Malware', 'Normal'))

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.show()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        name_of_datafile = sys.argv[1]

        (number_of_malware, number_of_normal, title, x_axis, y_axis) = read_plot_data_file(name_of_datafile)
        print "Malwares: ", number_of_malware
        print "Normal: ", number_of_normal
        create_plot(title, x_axis, y_axis)
    else:
        print "Error: There must be exactly one argument as name of the data file."
