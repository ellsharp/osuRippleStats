import sys
import os
from ors.script.ripple_api import RippleApi
from ors.script import converter
from ors.script import database
from ors.script import logger

if __name__ == "__main__":
    from ors.main.users_stats_transaction import UsersStatsTransaction
    UsersStatsTransaction().execute()

class UsersStatsTransaction(object):
    global log
    log = logger.logger('UsersStatsTransaction')

    def execute(self):
        self.__set_users_stats_transaction()

    def __set_users_stats_transaction(self):
        result = database.execute_statement('t_users_stats_I01')
