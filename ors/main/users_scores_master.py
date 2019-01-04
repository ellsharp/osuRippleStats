import sys
import os
from ors.script.ripple_api import RippleApi
from ors.script import converter
from ors.script import database
from ors.script import logger

if __name__ == "__main__":
    from ors.main.users_scores_master import UsersScoresMaster
    UsersScoresMaster().execute()

class UsersScoresMaster(object):
    global log
    log = logger.logger('UsersScoresMaster')

    def execute(self):
        new_scores = self.__get_users_scores_transaction()
        self.__set_users_scores_master(new_scores)

    def __get_users_scores_transaction(self):
        result = database.execute_statement('t_users_scores_S01')
        return result[1]

    def __set_users_scores_master(self, new_scores):
        for new_score in new_scores:
            result = database.execute_statement('m_users_scores_S01', new_score['user_id'], new_score['beatmap_md5'])
            master_score = result[1]
            if bool(master_score) == False:
                del new_score['updated_on']
                result = database.execute_statement_values('m_users_scores_I01', new_score.values())
                result = database.execute_statement('m_beatmaps_S01', new_score['beatmap_md5'])
                song_name = result[1][0]['song_name']
                log.info('ORSI0003', new_score['user_id'], new_score['score_id'], song_name, new_score['score'], new_score['rank'])
                ranking = self.__get_scores_ranking(new_score)
                self.__set_users_activity(new_score, ranking)
            else:
                master_score = master_score[0]
                master_scores_score = master_score['score']
                new_scores_score = new_score['score']
                if new_scores_score > master_scores_score:
                    del new_score['created_on']
                    del new_score['updated_on']
                    new_score.update(beatmap_md5_key=new_score['beatmap_md5'])
                    result = database.execute_statement_values('m_users_scores_U01', new_score.values())
                    result = database.execute_statement('m_beatmaps_S01', new_score['beatmap_md5'])
                    song_name = result[1][0]['song_name']
                    log.info('ORSI0004', new_score['user_id'], new_score['score_id'], song_name, new_score['score'], new_score['rank'])
                    ranking = self.__get_scores_ranking(new_score)
                    self.__set_users_activity(new_score, ranking)
                result = database.execute_statement('m_beatmaps_S01', new_score['beatmap_md5'])
                song_name = result[1][0]['song_name']
                log.info('ORSI0005', new_score['user_id'], new_score['score_id'], song_name, new_score['score'], new_score['rank'])

    def __get_scores_ranking(self, score_dict):
        ripple_api = RippleApi()
        leaderboard_scores = ripple_api.get_leaderboard(score_dict['beatmap_md5'], score_dict['play_mode'])
        leaderboard_scores = leaderboard_scores['scores']
        score_id = score_dict['score_id']
        score = score_dict['score']
        counter = 1
        for leaderboard_score in leaderboard_scores:
            leaderboard_scores_score = leaderboard_score['score']
            leaderboard_score_id = leaderboard_score['id']
            leaderboard_user_id = leaderboard_score['user']['id']
            score_user_id = score_dict['user_id']
            if score_id == leaderboard_score_id:
                break;
            else:
                if score > leaderboard_scores_score:
                    break;
                else:
                    if leaderboard_user_id == score_user_id:
                        break;
                    else:
                        counter = counter + 1
        return counter

    def __set_users_activity(self, score, ranking):
        beatmap_md5 = score['beatmap_md5']
        result = database.execute_statement('m_beatmaps_S02', beatmap_md5)
        beatmap_id = result[1][0]['beatmap_id']
        song_name = result[1][0]['song_name']
        activity = converter.convert_activity(score, beatmap_id, song_name, ranking)
        # Duplicate check
        result = database.execute_statement('t_users_activity_S01', activity['score_id'])
        count = result[0]
        if count == 0:
            result = database.execute_statement_values('t_users_activity_I01', activity.values())
