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
            self.__set_users_scores_transaction()
            connection.commit()
            connection.close()
            log.info('ORSI0002', 'UsersScoresTransaction')
        except Exception as e:
            log.critical('ORSC0001', 'UsersScoresTransaction', e)
            raise Exception(e)

    def __set_users_scores_transaction(self):
        result = database.execute_statement(connection, 't_users_scores_I01')
        log.debug('ORSD0006', 't_users_scores', result[0])
