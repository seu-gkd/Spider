import inspect
import os
import sys


def get_root_path():
    file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
    parent_path = os.path.dirname(file_path)
    root_path = os.path.dirname(parent_path)
    return root_path


def create_data_path():
    root_path = get_root_path()
    data_path = root_path + "/data"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return data_path


def create_date_path(date):
    data_path = create_data_path()
    date_path = data_path + "/" + date
    if not os.path.exists(date_path):
        os.makedirs(date_path)
    return date_path


def create_type_path(type, date):
    date_path = create_date_path(date)
    type_path = date_path + "/" + type
    if not os.path.exists(type_path):
        os.makedirs(type_path)
    return type_path


ROOT_PATH = get_root_path()
DATA_PATH = ROOT_PATH + "/data"
SAMPLE_PATH = ROOT_PATH + "/sample"
LOG_PATH = ROOT_PATH + "/log"

if __name__ == '__main__':
    print(get_root_path())
