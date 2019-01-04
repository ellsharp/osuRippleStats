import sys
import os
from ors.script.ripple_api import RippleApi
from ors.script import converter
from ors.script import database
from ors.script import logger

if __name__ == "__main__":
    from ors.main.users_scores_transaction import UsersScoresTransaction
    UsersScoresTransaction().execute()

class UsersScoresTransaction(object):
    global log
    log = logger.logger('UsersScoresTransaction')

    def __init__(self):
        self.logger = logger.logger('UsersScoresTransaction')

    def execute(self):
        self.__set_users_scores_transaction()

    def __set_users_scores_transaction(self):
        result = database.execute_statement('t_users_scores_I01')
