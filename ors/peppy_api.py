import traceback
import requests
import pymysql
import sys
import os
from ors import util
from ors import core
from ors.logger import logger

logger = logger(str(os.path.basename(__file__)))

def get_user(user_id, mode):
    global logger
    config = util.get_config_object()
    api_url = config['url']['get_user']
    api_parameters = {'u': user_id, 'm': mode}
    try:
        logger.info('Try to GET /get_user peppy api.')
        api_response = requests.get(api_url, params=api_parameters)
        response = api_response.json()
        logger.info('Try to GET /get_user peppy api has succeeded.')
        return response
    except Exception as e:
        logger.critical('Failed to GET /get_user peppy api. Exception[%s]\n %s' % (e, traceback.format_exc()))
        sys.exit(1)

def get_beatmaps(beatmap_md5, mode, converted, limit):
    config = util.get_config_object()
    api_url = config['url']['get_beatmaps']
    api_parameters = {'m': mode, 'a': converted, 'h': beatmap_md5, 'limit': limit}
    try:
        api_response = requests.get(api_url, params=api_parameters)
        response = api_response.json()
        return response
    except Exception as e:
        logger.critical('Failed to GET /get_user peppy api. Exception[%s]\n %s' % (e, traceback.format_exc()))
        sys.exit(1)
