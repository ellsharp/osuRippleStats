import sys
import os
from ors.script.database import Database
from ors.script import converter
from ors.script import logger

if __name__ == "__main__":
    from ors.main.users_stats_transaction import UsersStatsTransaction
    UsersStatsTransaction().execute()

class UsersStatsTransaction(object):
    global log
    global database
    global connection
    log = logger.logger('users_stats_transaction')
    database = Database()
    connection = database.get_connection()

    def execute(self):
        try:
            log.info('ORSI0001', 'UsersStatsTransaction')
            user_ids = self.__get_target_user_ids()
            for __user_id in user_ids:
                user_id = __user_id['user_id']
                self.__set_users_stats_transaction(user_id)
                self.__set_users_badges(user_id)
                self.__set_users_silence_info(user_id)
            connection.commit()
            connection.close()
            log.info('ORSI0002', 'UsersStatsTransaction')
        except Exception as e:
            log.critical('ORSC0001', 'UsersStatsTransaction', e)
            raise Exception(e)

    def __get_target_user_ids(self):
        result = database.execute_statement(connection, 'm_users_003')
        user_ids = result[1]
        return user_ids

    def __set_users_stats_transaction(self, user_id):
        result = database.execute_statement(connection, 't_users_stats_I01', user_id)
        log.debug('ORSD0002', 't_users_stats', result[0], user_id)

    def __set_users_badges(self, user_id):
        result = database.execute_statement(connection, 't_users_badges_I01', user_id)
        log.debug('ORSD0002', 't_users_badges', result[0], user_id)

    def __set_users_silence_info(self, user_id):
        result = database.execute_statement(connection, 't_users_silence_info_I01', user_id)
        log.debug('ORSD0002', 't_users_silence_info', result[0], user_id)
