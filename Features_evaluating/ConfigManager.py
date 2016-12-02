import ConfigParser
import glob
import os

def find_name_of_searched_file():
    """
    This method finds searched file and returns path with name of that file.
    """
    searched_file = glob.glob('*.cfg')
    if len(searched_file) > 1 or len(searched_file) == 0:
        return -1
    return searched_file[0]


def read_config():
    """
    It reads path to single data set from config file.
    """
    name_of_config = find_name_of_searched_file()
    config = ConfigParser.ConfigParser(allow_no_value=True)
    try:
        config.read(name_of_config)
    except TypeError:
        print "Error: In current folder there is no *.cfg file or there are more cfg files. For help, see README.md."

    try:
        single_path = config.get('PATHS', 'path_to_single_dataset')
        multi_path = config.get('PATHS', 'path_to_multi_dataset')
        return single_path, multi_path
    except ConfigParser.Error:
        print "Error: Set correct your config file! For more information see README.md."
        return -1


def get_folders_in_multi(my_path):
    """
    This method goes into 'multi data set', where has to at least on folder as 'single data set'
    For more information see README.md
    :return: list of names folders(single data sets)
    """
    return os.listdir(my_path)