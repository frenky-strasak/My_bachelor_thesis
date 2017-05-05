import sys
import os


"""
Read dataset_times.txt
"""
path_to_datset_times = "c:/Users/frenk/Documents/Skola/Bachelor_thesis/dataset_times.txt"

dataset_name_dict = dict()
try:
    with open(path_to_datset_times) as f:
        for line in f:
            split = line.split('	')
            datset_name = split[1]
            unix_time = float(split[2].rstrip())
            if unix_time == 0:
                continue
            print datset_name, unix_time
            dataset_name_dict[datset_name] = unix_time
    f.close()
except:
    print "Error: no dataset_names.txt"


my_path = sys.argv[1]
datasets = os.listdir(my_path)
for dataset in datasets:
    print "-----------", dataset, "---------------"
    final_path = my_path + dataset
    try:
        if dataset_name_dict[dataset]:
            with open(final_path + "\\start_date.txt", 'w') as f:
                print "INFO: started_date.txt was added... ", final_path
                f.write("# Unix time of started date\n")
                f.write(str(dataset_name_dict[dataset]))
            f.close()
    except:
        print "Error: This dataset has right format of time. No date.txt was added."

