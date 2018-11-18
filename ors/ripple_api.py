import traceback
import requests
import pymysql
import sys
import os
from ors import util
from ors import core
from ors.logger import logger

logger = logger(str(os.path.basename(__file__)))

def get_ping(ripple_token):
    """
    Check the ripple is alive.
    """
    global logger
    config = util.get_config_object()
    api_url = config['url']['ping']
    api_parameters = {'X-Ripple-Token': ripple_token}
    try:
        logger.info('Try to GET /ping ripple api.')
        api_response = requests.get(api_url)
        response = api_response.json()
        if (util.is_ripple_api_access_succeeded(response)):
            logger.info('Try to GET /ping ripple api has succeeded.')
            return response
        else:
            raise Exception('Ripple api returns abnormal code.')
    except Exception as e:
        logger.critical('Failed to GET /ping ripple api. Exception[%s]\n %s' % (e, traceback.format_exc()))
        sys.exit(1)

def get_users_scores_best(ripple_token, id, mode, l):
    global logger
    config = util.get_config_object()
    api_url = config['url']['users_scores_recent']
    api_parameters = {'X-Ripple-Token': ripple_token, 'id': id, 'mode': mode, 'l': l}
    try:
        logger.info('Try to GET /users/scores/recent ripple api.')
        api_response = requests.get(api_url, params=api_parameters)
        response = api_response.json()
        if (util.is_ripple_api_access_succeeded(response)):
            logger.info('Try to GET /users/scores/recent ripple api has succeeded.')
            return response
        else:
            raise Exception('Ripple api returns abnormal code.')
    except Exception as e:
        logger.critical('Failed to GET /users/scores/recent ripple api. Exception[%s]\n %s' % (e, traceback.format_exc()))
        sys.exit(1)

def get_users_scores_recent(ripple_token, user_id, mode, l):
    global logger
    config = util.get_config_object()
    api_url = config['url']['users_scores_recent']
    api_parameters = {'X-Ripple-Token': ripple_token, 'id': user_id, 'mode': mode, 'l': l}
    try:
        logger.info('Try to GET /users/scores/recent ripple api.')
        api_response = requests.get(api_url, params=api_parameters)
        response = api_response.json()
        if (util.is_ripple_api_access_succeeded(response)):
            logger.info('Try to GET /users/scores/recent ripple api has succeeded.')
            # Returns only scores, without code.
            return response['scores']
        else:
            raise Exception('Ripple api returns abnormal code.')
    except Exception as e:
        logger.critical('Failed to GET /users/scores/recent ripple api. Exception[%s]\n %s' % (e, traceback.format_exc()))
        sys.exit(1)

def get_users_full(ripple_token, id):
    global logger
    config = util.get_config_object()
    api_url = config['url']['users_full']
    api_parameters = {'X-Ripple-Token': ripple_token, 'id': id}
    try:
        logger.info('Try to GET /users/full ripple api.')
        api_response = requests.get(api_url, params=api_parameters)
        response = api_response.json()
        if (util.is_ripple_api_access_succeeded(response)):
            logger.info('Try to GET /users/full ripple api has succeeded.')
            return response
        else:
            raise Exception('Ripple api returns abnormal code.')
    except Exception as e:
        logger.critical('Failed to GET /users/full ripple api. Exception[%s]\n %s' % (e, traceback.format_exc()))
        sys.exit(1)

def get_scores(ripple_token, beatmap_md5, pagination, mode, sorting):
    """
    Retrieves scores for a certain beatmap.
    """
    config = util.get_config_object()
    api_url = config['url']['scores']
    api_parameters = {'X-Ripple-Token': ripple_token, 'md5': beatmap_md5, 'l': pagination, 'mode': mode, 'sort': sorting}
    try:
        logger.info('Try to GET /scores ripple api.')
        api_response = requests.get(api_url, params=api_parameters)
        response = api_response.json()
        print(response)
        if (util.is_ripple_api_access_succeeded(response)):
            logger.info('Try to GET /scores ripple api has succeeded.')
            return response['scores']
        else:
            raise Exception('Ripple api returns abnormal code.')
    except Exception as e:
        logger.critical('Failed to GET /scores ripple api. Exception[%s]\n %s' % (e, traceback.format_exc()))
        sys.exit(1)
