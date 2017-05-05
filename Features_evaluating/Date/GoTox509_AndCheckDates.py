import sys
import os
import datetime

def load_x509_file(path_to_dataset, cert_dict):

    """
    Read started timestamp if this current dataset was indexed from 1970
    Try to read "start_date.txt", if is there this file, we have to read start timestamp from this file
    If not the timedate is in right format.
    """
    started_unix_time = 0.0
    try:
        with open(path_to_dataset + "\\start_date.txt") as f:
            started_unix_time = float(f.readlines()[1])
        f.close()
    except:
        print "Error: no started_date.txt file."


    count_lines = 0
    right = 0
    not_right = 0
    average_list = []
    try:
        with open(path_to_dataset + "\\bro\\x509.log") as f:
            # go thru ssl file line by line and for each ssl line check all uid of flows
            for line in f:
                if '#' == line[0]:
                    continue
                split = line.split('	')
                x509_uid = split[1]
                cert_serial = split[3]

                try:
                    if cert_dict[cert_serial]:
                        continue
                except:
                    cert_dict[cert_serial] = 1

                current_time = float(split[0]) + started_unix_time
                before_date = float(split[6])
                after_date = float(split[7])

                if current_time > before_date and current_time < after_date:
                    right += 1
                else:
                    not_right += 1

                average_list.append(current_time)
                count_lines += 1
        f.close()
    except IOError:
        print "Error: No x509 file."
        # print "len dict of x509", len(self.x509_dict)
        # __PrintManager__.processLog_number_of_addes_x509(count_lines)

    print "in date range:", right
    print "out date range:", not_right
    print "lines:", count_lines
    if len(average_list) != 0:
        temp = 0.0
        for a in average_list:
            temp += a
        average = temp / len(average_list)
        print datetime.datetime.fromtimestamp(average).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        cert_dict = dict()
        my_path = sys.argv[1]
        datasets = os.listdir(my_path)
        index = 1
        for dataset in datasets:
            print "-----------", index, "/", len(datasets),  dataset, "---------------"
            path_to_dataset = my_path + dataset
            # print path_to_dataset
            load_x509_file(path_to_dataset, cert_dict)

            index += 1

        print "-----------------------------------------"
        print "all cert:", len(cert_dict.keys())