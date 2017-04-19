

import sys
import os
import shutil

def check_dataset(directory_name):
    if not(os.path.isfile(directory_name + "/bro/ssl.log")):
        print directory_name
        # shutil.rmtree(directory_name) #Delete !!!!

    # if os.path.exists(directory_name):
    #     shutil.rmtree(directory_name)
    # os.makedirs(directory_name)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        path = sys.argv[1]

        datasets_paths = os.listdir(path)
        for i in range(len(datasets_paths)):
            # print datasets_paths[i]
            check_dataset(path + datasets_paths[i])
