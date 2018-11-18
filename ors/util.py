import configparser
import traceback
import pymysql
import time
import pytz
import sys
import os
from datetime import timezone
from datetime import datetime
from ors import util
from ors.logger import logger
from ors import ripple_api

logger = logger(str(os.path.basename(__file__)))

def get_config_object():
    """
    Read config file objevt and returns it.
    """
    try:
        logger.debug('Try to read config file.')
        config_file_path = 'conf/ors.conf'
        config_object = configparser.ConfigParser()
        config_object.read(config_file_path, 'utf-8')
        logger.debug('Try to read config file has succeeded.')
        return config_object
    except Exception as e:
        logger.critical('Failed to read config file. Exception[%s]\n %s' % (e, traceback.format_exc()))
        sys.exit(1)


def convert_scores_data(user_id, scores_data):
    """
    Convert users scores data to format of database.
    """
    converted_scores_data = []
    for read_data in scores_data:
        temp_data = {}
        temp_data['user_id'] = user_id
        temp_data['score_id'] = read_data['id']
        temp_data['beatmap_md5'] = read_data['beatmap_md5']
        temp_data['max_combo'] = read_data['max_combo']
        temp_data['score'] = read_data['score']
        temp_data['is_full_combo'] = int(read_data['full_combo'])
        temp_data['mods'] = read_data['mods']
        temp_data['count_300'] = read_data['count_300']
        temp_data['count_100'] = read_data['count_100']
        temp_data['count_50'] = read_data['count_50']
        temp_data['count_geki'] = read_data['count_geki']
        temp_data['count_katu'] = read_data['count_katu']
        temp_data['count_miss'] = read_data['count_miss']
        temp_data['time'] = str(util.get_utc_datetime_from_iso(read_data['time']))
        temp_data['play_mode'] = read_data['play_mode']
        temp_data['accuracy'] = read_data['accuracy']
        temp_data['pp'] = read_data['pp']
        temp_data['rank'] = read_data['rank']
        temp_data['completed'] = read_data['completed']
        temp_data['created_on'] = str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
        temp_data['created_by'] = str(os.path.basename(__file__))
        temp_data['updated_by'] = str(os.path.basename(__file__))
        converted_scores_data.append(temp_data)
    return converted_scores_data

def convert_stats_data(user_id, stats_data, mode):
    """
    Convert users stats data to format of database.
    """
    mode_name = util.get_mode_name(mode)
    converted_stats_data = {}
    converted_stats_data['user_id'] = stats_data['id']
    converted_stats_data['username'] = stats_data['username']
    converted_stats_data['username_aka'] = stats_data['username_aka']
    converted_stats_data['registered_on'] = str(util.get_utc_datetime_from_iso(stats_data['registered_on']))
    converted_stats_data['privileges'] = stats_data['privileges']
    converted_stats_data['latest_activity'] =  str(util.get_utc_datetime_from_iso(stats_data['latest_activity']))
    converted_stats_data['country'] = stats_data['country']
    converted_stats_data['ranked_score'] = stats_data[mode_name]['ranked_score']
    converted_stats_data['total_score'] = stats_data[mode_name]['total_score']
    converted_stats_data['playcount'] = stats_data[mode_name]['playcount']
    converted_stats_data['replays_watched'] = stats_data[mode_name]['replays_watched']
    converted_stats_data['total_hits'] = stats_data[mode_name]['total_hits']
    converted_stats_data['level'] = stats_data[mode_name]['level']
    converted_stats_data['accuracy'] = stats_data[mode_name]['accuracy']
    converted_stats_data['pp'] = stats_data[mode_name]['pp']
    converted_stats_data['global_leaderboard_rank'] = stats_data[mode_name]['global_leaderboard_rank']
    converted_stats_data['country_leaderboard_rank'] = stats_data[mode_name]['country_leaderboard_rank']
    converted_stats_data['play_style'] = stats_data['play_style']
    converted_stats_data['favourite_mode'] = stats_data['favourite_mode']
    converted_stats_data['created_on'] = str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
    converted_stats_data['created_by'] = str(os.path.basename(__file__))
    converted_stats_data['updated_by'] = str(os.path.basename(__file__))
    return converted_stats_data

def convert_beatmap_data(beatmap_data):
    """
    Convert beatmap data to format of database.
    """
    beatmap_data['created_on'] = str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
    beatmap_data['created_by'] = str(os.path.basename(__file__))
    beatmap_data['updated_by'] = str(os.path.basename(__file__))
    return beatmap_data

def is_ripple_api_access_succeeded(ripple_api_response_json):
    """
    Checks return code from ripple api.
    """
    logger.debug('Try to check ripple api returns code.')
    code = ripple_api_response_json['code']
    logger.debug('Ripple api returns code [%s]' % code)
    if (code == 200):
        return True
    else:
        return False

def is_first_place_ranks(user_id, beatmap_md5, mode):
    """
    Access to ripple api and get scores and judge first place ranks.
    """
    config = util.get_config_object()
    ripple_token = config['token']['X-Ripple-Token']
    scores = ripple_api.get_scores(ripple_token, beatmap_md5, '1', mode, 'score')
    time.sleep(1)
    try:
        first_place_user_id = scores[0]['user']['id']
    except Exception as e:
        return False
    if (int(user_id) == int(first_place_user_id)):
        return True
    else:
        return False

def get_users_scores_master_table_name(mode):
    """
    Returns m_users_scores_[mode] table name.
    """
    if (mode == 0):
        return 'm_users_scores_std'
    elif (mode == 1):
        return 'm_users_scores_taiko'
    elif (mode == 2):
        return 'm_users_scores_ctb'
    elif (mode == 3):
        return 'm_users_scores_mania'
    else:
        logger.critical('Unexpected argument[%s] is given in method[%s]' % (mode, sys._getframe().f_code.co_name))
        sys.exit(1)

def get_users_scores_transaction_table_name(mode):
    """
    Returns t_users_scores_[mode] table name.
    """
    if (mode == 0):
        return 't_users_scores_std'
    elif (mode == 1):
        return 't_users_scores_taiko'
    elif (mode == 2):
        return 't_users_scores_ctb'
    elif (mode == 3):
        return 't_users_scores_mania'
    else:
        logger.critical('Unexpected argument[%s] is given in method[%s]' % (mode, sys._getframe().f_code.co_name))
        sys.exit(1)

def get_users_scores_work_table_name(mode):
    """
    Returns w_users_scores_[mode] table name.
    """
    if (mode == 0):
        return 'w_users_scores_std'
    elif (mode == 1):
        return 'w_users_scores_taiko'
    elif (mode == 2):
        return 'w_users_scores_ctb'
    elif (mode == 3):
        return 'w_users_scores_mania'
    else:
        logger.critical('Unexpected argument[%s] is given in method[%s]' % (mode, sys._getframe().f_code.co_name))
        sys.exit(1)

def get_users_stats_master_table_name(mode):
    """
    Returns m_users_stats_[mode] table name.
    """
    if (mode == 0):
        return 'm_users_stats_std'
    elif (mode == 1):
        return 'm_users_stats_taiko'
    elif (mode == 2):
        return 'm_users_stats_ctb'
    elif (mode == 3):
        return 'm_users_stats_mania'
    else:
        logger.critical('Unexpected argument[%s] is given in method[%s]' % (mode, sys._getframe().f_code.co_name))
        sys.exit(1)

def get_users_stats_transaction_table_name(mode):
    """
    Returns t_users_stats_[mode] table name.
    """
    if (mode == 0):
        return 't_users_stats_std'
    elif (mode == 1):
        return 't_users_stats_taiko'
    elif (mode == 2):
        return 't_users_stats_ctb'
    elif (mode == 3):
        return 't_users_stats_mania'
    else:
        logger.critical('Unexpected argument[%s] is given in method[%s]' % (mode, sys._getframe().f_code.co_name))
        sys.exit(1)

def get_users_stats_work_table_name(mode):
    """
    Returns w_users_stats_[mode] table name.
    """
    if (mode == 0):
        return 'w_users_stats_std'
    elif (mode == 1):
        return 'w_users_stats_taiko'
    elif (mode == 2):
        return 'w_users_stats_ctb'
    elif (mode == 3):
        return 'w_users_stats_mania'
    else:
        logger.critical('Unexpected argument[%s] is given in method[%s]' % (mode, sys._getframe().f_code.co_name))
        sys.exit(1)

def get_beatmaps_table_name(mode):
    """
    Returns m_beatmaps_[mode] table name.
    """
    if (mode == 0):
        return 'm_beatmaps_std'
    elif (mode == 1):
        return 'm_beatmaps_taiko'
    elif (mode == 2):
        return 'm_beatmaps_ctb'
    elif (mode == 3):
        return 'm_beatmaps_mania'
    else:
        logger.critical('Unexpected argument[%s] is given in method[%s]' % (mode, sys._getframe().f_code.co_name))
        sys.exit(1)

def get_first_place_table_name(mode):
    """
    Returns m_first_place_[mode] table name.
    """
    if (mode == 0):
        return 'm_first_place_std'
    elif (mode == 1):
        return 'm_first_place_taiko'
    elif (mode == 2):
        return 'm_first_place_ctb'
    elif (mode == 3):
        return 'm_first_place_mania'
    else:
        logger.critical('Unexpected argument[%s] is given in method[%s]' % (mode, sys._getframe().f_code.co_name))
        sys.exit(1)

def get_mode_name(mode):
    """
    Returns mode name from inputted mode number.
    """
    if (mode == 0):
        return 'std'
    elif (mode == 1):
        return 'taiko'
    elif (mode == 2):
        return 'ctb'
    elif (mode == 3):
        return 'mania'
    else:
        logger.critical('Unexpected argument[%s] is given in method[%s]' % (mode, sys._getframe().f_code.co_name))
        sys.exit(1)

def get_utc_datetime_from_iso(iso_str):
    dt = None
    if ":" == iso_str[-3:-2]:
        iso_str = iso_str[:-3]+iso_str[-2:]
    try:
        dt = datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%S%Z')
        dt = pytz.utc.localize(dt).astimezone(pytz.timezone('UTC'))
    except ValueError:
        try:
            dt = datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%S%z')
            dt = dt.astimezone(pytz.timezone('UTC'))
        except ValueError:
            pass
    return dt.strftime('%Y-%m-%d %H:%M:%S')
