from ors.script import ripple_api
from ors.script import util
import requests
import time
import sys
from ors.script import logger

if __name__ == "__main__":
    ripple_api = ripple_api.RippleApi()
    print(ripple_api.get_users_scores_recent(70666, 0))

class RippleApi(object):
    global log
    log = logger.logger('RippleApi')
    config = ''
    ripple_token = ''

    def __init__(self):
        self.config = util.read_config()
        self.ripple_token = self.config['token']['X-Ripple-Token']

    def get_ping(self):
        """
        Check the Ripple is alive.
        """
        api_url = self.config['url']['ping']
        try:
            api_response = requests.get(api_url)
            response = api_response.json()
        except Exception as e:
            sys.exit(1)
        # Wait a second to don't get a high load on Ripple API.
        time.sleep(1)
        return response

    def get_users_full(self, user_id):
        api_url = self.config['url']['users_full']
        api_parameters = {'X-Ripple-Token': self.ripple_token, 'id': user_id}
        response = self.get_api_response(api_url, api_parameters)
        return response

    def get_users_scores_recent(self, user_id, mode):
        api_url = self.config['url']['users_scores_recent']
        api_parameters = {'X-Ripple-Token': self.ripple_token, 'id': user_id, 'mode': mode, 'l': 100}
        response = self.get_api_response(api_url, api_parameters)
        return response

    def get_leaderboard(self, beatmap_md5, mode):
        api_url = self.config['url']['scores']
        api_parameters = {'X-Ripple-Token': self.ripple_token, 'md5': beatmap_md5, 'mode': mode, 'l': 50, 'sort': 'score'}
        response = self.get_api_response(api_url, api_parameters)
        return response

    def get_api_response(self, api_url, api_parameters):
        retry_count = 2
        for i in range(3):
            try:
                api_response = requests.get(api_url, params=api_parameters)
                response = api_response.json()
                # Check Ripple API's return code.
                response_code = response['code']
                if response_code == 200:
                    log.debug('ORSD0003', api_url, api_parameters)
                    break;
                else:
                    log.error('ORSE0002', response_code, retry_count, api_url, api_parameters)
            except Exception as e:
                    log.error('ORSE0001', retry_count, e, api_url, api_parameters)
            if retry_count > 0:
                retry_count = retry_count - 1
                time.sleep(60)
            else:
                log.critical('ORSC0002', api_url, api_parameters)
                sys.exit(1)
        time.sleep(1)
        return response
