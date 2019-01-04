import sys
import os
from ors.script.database import Database
from ors.script.ripple_api import RippleApi
from ors.script import converter
from ors.script import logger

if __name__ == "__main__":
    from ors.main.users_scores_master import UsersScoresMaster
    UsersScoresMaster().execute()

class UsersScoresMaster(object):
    global log
    global database
    global connection
    log = logger.logger('users_scores_master')
    database = Database()
    connection = database.get_connection()

    def execute(self):
        log.info('ORSI0001', 'UsersScoresMaster')
        user_ids = self.__get_target_user_ids()
        for __user_id in user_ids:
            user_id = __user_id['user_id']
            new_scores = self.__get_users_scores_transaction(user_id)
            self.__set_users_scores_master(new_scores, user_id)
        connection.commit()
        connection.close()
        log.info('ORSI0002', 'UsersScoresMaster')

    def __get_target_user_ids(self):
        result = database.execute_statement(connection, 'm_users_003')
        user_ids = result[1]
        return user_ids

    def __get_users_scores_transaction(self, user_id):
        result = database.execute_statement(connection, 't_users_scores_S01', user_id)
        log.debug('ORSD0010', 't_users_scores', result[0], user_id)
        return result[1]

    def __set_users_scores_master(self, new_scores, user_id):
        new_counter = 0
        updated_counter = 0
        not_updated_counter = 0
        for new_score in new_scores:
            result = database.execute_statement(connection, 'm_users_scores_S01', user_id, new_score['beatmap_md5'])
            master_score = result[1]
            if bool(master_score) == False:
                # Case of new score.
                del new_score['is_on_master']
                del new_score['is_on_activity']
                del new_score['updated_on']
                result = database.execute_statement_values(connection, 'm_users_scores_I01', new_score.values())
                result = database.execute_statement(connection, 'm_beatmaps_S01', new_score['beatmap_md5'])
                song_name = result[1][0]['song_name']
                log.debug('ORSD0011', new_score['user_id'], new_score['score_id'], song_name, new_score['score'], new_score['rank'])
                # Mark the score has processed on transaction.
                result = database.execute_statement(connection, 't_users_scores_U01', new_score['score_id'])
                new_counter = new_counter + 1
            else:
                # Case of updated or not score.
                master_score = master_score[0]
                master_scores_score = master_score['score']
                new_scores_score = new_score['score']
                if new_scores_score > master_scores_score:
                    # Case of updated score.
                    del new_score['is_on_master']
                    del new_score['is_on_activity']
                    del new_score['created_on']
                    del new_score['updated_on']
                    new_score.update(beatmap_md5_key=new_score['beatmap_md5'])
                    result = database.execute_statement_values(connection, 'm_users_scores_U01', new_score.values())
                    result = database.execute_statement(connection, 'm_beatmaps_S01', new_score['beatmap_md5'])
                    song_name = result[1][0]['song_name']
                    log.debug('ORSD0012', new_score['user_id'], new_score['score_id'], song_name, new_score['score'], new_score['rank'])
                    # Mark the score has processed on transaction.
                    result = database.execute_statement(connection, 't_users_scores_U01', new_score['score_id'])
                    updated_counter = updated_counter + 1
                else:
                    # Case of not updated score.
                    result = database.execute_statement(connection, 'm_beatmaps_S01', new_score['beatmap_md5'])
                    song_name = result[1][0]['song_name']
                    log.debug('ORSD0013', new_score['user_id'], new_score['score_id'], song_name, new_score['score'], new_score['rank'])
                    # Mark the score has processed on transaction.
                    result = database.execute_statement(connection, 't_users_scores_U01', new_score['score_id'])
                    not_updated_counter = not_updated_counter + 1;
        log.info('ORSI0010', new_counter, updated_counter, not_updated_counter)

"""
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
"""
