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


def create_site_path(site):
    data_path = create_data_path()
    site_path = data_path + "/" + site
    if not os.path.exists(site_path):
        os.makedirs(site_path)
    return site_path


def create_city_path(site, city):
    site_path = create_site_path(site)
    city_path = site_path + "/" + city
    if not os.path.exists(city_path):
        os.makedirs(city_path)
    return city_path


def create_date_path(site, city, date):
    city_path = create_city_path(site, city)
    date_path = city_path + "/" + date
    if not os.path.exists(date_path):
        os.makedirs(date_path)
    return date_path


ROOT_PATH = get_root_path()
DATA_PATH = ROOT_PATH + "/data"
SAMPLE_PATH = ROOT_PATH + "/sample"
LOG_PATH = ROOT_PATH + "/log"

if __name__ == '__main__':
    print(get_root_path())
