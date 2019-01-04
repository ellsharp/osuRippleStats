import configparser
from datetime import datetime
import pytz

def read_config():
    config_file_path = 'conf/ors.conf'
    config_object = configparser.ConfigParser()
    config_object.read(config_file_path, 'utf-8')
    return config_object

def datetime_now():
    return datetime.now(pytz.timezone('UTC'))
