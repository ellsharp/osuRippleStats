import configparser
from datetime import datetime
from ors.script import converter
import pytz

def read_config():
    config_file_path = 'conf/ors.conf'
    config_object = configparser.ConfigParser()
    config_object.read(config_file_path, 'utf-8')
    return config_object

def datetime_now():
    return datetime.now(pytz.timezone('UTC'))

def datetime_now_str():
    return datetime.now(pytz.timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S')

def get_beatmap_info(beatmap_md5, mode):
    from ors.script.database import Database
    database = Database()
    connection = database.get_connection()
    result = database.execute_statement(connection, 'm_beatmaps_S01', beatmap_md5)
    count = result[0]
    if count == 0:
        from ors.script.ripple_api import RippleApi
        ripple_api = RippleApi()
        beatmap_info = ripple_api.get_beatmap_info(beatmap_md5, mode)
        beatmap_info = converter.convert_beatmap_peppy(beatmap_info[0])
        result = database.execute_statement_values(connection, 'm_beatmaps_I01', beatmap_info.values())
        connection.commit()
        connection.close()
        return beatmap_info
    else:
        return result[1][0]

def count_up_api_request():
    from ors.script.database import Database
    from ors.script import util
    database = Database()
    connection = database.get_connection()
    now = util.datetime_now_str()
    result = database.execute_statement(connection, 's_api_request_count_tick_S01', now)
    is_exists = result[0]
    if is_exists == 0:
        result = database.execute_statement(connection, 's_api_request_count_tick_I01', now)
    else:
        count = result[1][0]['count']
        count = count + 1
        result = database.execute_statement(connection, 's_api_request_count_tick_U01', count, now)
    connection.commit()
    connection.close()
