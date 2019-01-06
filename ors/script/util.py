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
