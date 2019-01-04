import sys
import os
from ors.script.ripple_api import RippleApi
from ors.script import converter
from ors.script import database
from ors.script import logger

if __name__ == "__main__":
    from ors.main.users_scores_work import UsersScoresWork
    UsersScoresWork().execute()

class UsersScoresWork(object):
    global log
    log = logger.logger('UsersScoresWork')

    def __init__(self):
        self.logger = logger.logger('UsersScoresWork')

    def execute(self):
        user_ids = self.__get_target_user_ids()
        for __user_id in user_ids:
            mode = 0 # In debugging always standard mode
            user_id = __user_id['user_id']
            users_scores = self.__get_users_scores(user_id, mode)
            users_scores = users_scores['scores']
            self.__set_users_scores_work(user_id, users_scores, mode)
            self.__set_beatmaps_work(users_scores, mode)

    def __get_target_user_ids(self):
        result = database.execute_statement('m_users_S02')
        user_ids = result[1]
        return user_ids

    def __get_users_scores(self, user_id, mode):
        ripple_api = RippleApi()
        users_scores = ripple_api.get_users_scores_recent(user_id, mode)
        return users_scores

    def __set_users_scores_work(self, user_id, users_scores, mode):
        users_scores_temp = []
        for users_score in users_scores:
            users_score = converter.convert_users_score(user_id, users_score)
            users_scores_temp.append(users_score)
        users_scores = users_scores_temp
        result = database.execute_statement('w_users_scores_D01', user_id, mode)
        for users_score in users_scores:
            result = database.execute_statement_values('w_users_scores_I01', users_score.values())

    def __set_beatmaps_work(self, users_scores, mode):
        beatmaps = []
        for users_score in users_scores:
            beatmaps.append(users_score['beatmap'])
        result = database.execute_statement('w_beatmaps_D01')
        for beatmap in beatmaps:
            beatmap = converter.convert_beatmap(beatmap, mode)
            result = database.execute_statement_values('w_beatmaps_I01', beatmap.values())
