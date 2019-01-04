import sys
import os
from ors.script.ripple_api import RippleApi
from ors.script.database import Database
from ors.script import converter
from ors.script import logger

if __name__ == "__main__":
    from ors.main.users_stats_work import UsersStatsWork
    UsersStatsWork().execute()

class UsersStatsWork(object):
    global log
    global database
    global connection
    log = logger.logger('users_stats_work')
    database = Database()
    connection = database.get_connection()

    def execute(self):
        log.info('ORSI0001', 'UsersStatsWork')
        user_ids = self.__get_target_user_ids()
        for __user_id in user_ids:
            user_id = __user_id['user_id']
            users_stats = self.__get_users_stats(user_id)
            self.__set_users_stats_work(users_stats)
            self.__set_users_badge_work(user_id, users_stats)
            self.__set_users_silence_info_work(user_id, users_stats)
        connection.commit()
        connection.close()
        log.info('ORSI0002', 'UsersStatsWork')

    def __get_target_user_ids(self):
        result = database.execute_statement(connection, 'm_users_003')
        user_ids = result[1]
        return user_ids

    def __get_users_stats(self, user_id):
        ripple_api = RippleApi()
        users_stats = ripple_api.get_users_full(user_id)
        return users_stats

    def __set_users_stats_work(self, users_stats):
        users_stats = converter.convert_users_stats(users_stats)
        user_id = users_stats['user_id']
        result = database.execute_statement(connection, 'w_users_stats_D01', user_id)
        log.debug('ORSD0001', 'w_users_stats', result[0], user_id)
        result = database.execute_statement_values(connection, 'w_users_stats_I01', users_stats.values())
        log.debug('ORSD0002', 'w_users_stats', result[0], user_id)

    def __set_users_badge_work(self, user_id, users_stats):
        result = database.execute_statement(connection, 'w_users_badges_D01', user_id)
        log.debug('ORSD0001', 'w_users_badges', result[0], user_id)
        users_badges = users_stats['badges']
        users_custom_badge = users_stats['custom_badge']
        if users_badges != None:
            if users_custom_badge != None:
                users_custom_badge['id'] = 0
                users_badges.append(users_custom_badge)
            for users_badge in users_badges:
                users_badge = converter.convert_users_badge(user_id, users_badge)
                result = database.execute_statement_values(connection, 'w_users_badges_I01', users_badge.values())
                log.debug('ORSD0002', 'w_users_badges', result[0], user_id)

    def __set_users_silence_info_work(self, user_id, users_stats):
        users_silence_info = users_stats['silence_info']
        result = database.execute_statement(connection, 'w_users_silence_info_D01', user_id)
        log.debug('ORSD0001', 'w_users_silence_info', result[0], user_id)
        users_silence_info = converter.convert_users_silence_info(user_id, users_silence_info)
        result = database.execute_statement_values(connection, 'w_users_silence_info_I01', users_silence_info.values())
        log.debug('ORSD0002', 'w_users_silenfe_info', result[0], user_id)
