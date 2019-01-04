import sys
import os
from ors.script.ripple_api import RippleApi
from ors.script import converter
from ors.script import database
from ors.script import logger

if __name__ == "__main__":
    from ors.main.users_stats_master import UsersStatsMaster
    UsersStatsMaster().execute()

class UsersStatsMaster(object):
    global log
    log = logger.logger('UsersStatsMaster')

    def execute(self):
        user_ids = self.__get_target_user_ids()
        for __user_id in user_ids:
            user_id = __user_id['user_id']
            latest_stats = self.__get_users_latest_stats(user_id)
            self.__set_users_stats_master(latest_stats, user_id)

    def __get_target_user_ids(self):
        result = database.execute_statement('m_users_003')
        user_ids = result[1]
        return user_ids

    def __get_users_latest_stats(self, user_id):
        result = database.execute_statement('t_users_stats_S01', user_id)
        users_latest_stats = result[1]
        return users_latest_stats

    def __set_users_stats_master(self, latest_stats, user_id):
        result = database.execute_statement('m_users_stats_S01', user_id)
        count = result[1][0]['count']
        latest_stats = latest_stats[0]
        if count == 0:
            del latest_stats['updated_on']
            result = database.execute_statement_values('m_users_stats_I01', latest_stats.values())
        else:
            del latest_stats['created_on']
            del latest_stats['updated_on']
            latest_stats.update(user_id_key=latest_stats['user_id'])
            result = database.execute_statement_values('m_users_stats_U01', latest_stats.values())
