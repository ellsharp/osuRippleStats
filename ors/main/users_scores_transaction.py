import sys
import os
from ors.script.database import Database
from ors.script import converter
from ors.script import logger

if __name__ == "__main__":
    from ors.main.users_scores_transaction import UsersScoresTransaction
    UsersScoresTransaction().execute()

class UsersScoresTransaction(object):
    global log
    global database
    global connection
    log = logger.logger('Users_stats_transaction')
    database = Database()
    connection = database.get_connection()

    def execute(self):
        try:
            log.info('ORSI0001', 'UsersScoresTransaction')
            user_ids = self.__get_target_user_ids()
            for __user_id in user_ids:
                user_id = __user_id['user_id']
                self.__set_users_scores_transaction(user_id)
            connection.commit()
            connection.close()
            log.info('ORSI0002', 'UsersScoresTransaction')
        except Exception as e:
            log.critical('ORSC0001', 'UsersScoresTransaction', e)
            raise Exception(e)

    def __get_target_user_ids(self):
        result = database.execute_statement(connection, 'm_users_003')
        user_ids = result[1]
        return user_ids

    def __set_users_scores_transaction(self, user_id):
        result = database.execute_statement(connection, 't_users_scores_I01', user_id)
        log.debug('ORSD0002', 't_users_scores', result[0], user_id)
