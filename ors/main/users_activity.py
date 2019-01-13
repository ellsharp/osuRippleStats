import sys
import os
from ors.script.database import Database
from ors.script.ripple_api import RippleApi
from ors.script import converter
from ors.script import logger

if __name__ == "__main__":
    from ors.main.users_activity import UsersActivity
    UsersActivity().execute()

class UsersActivity(object):
    global log
    global database
    global connection
    log = logger.logger('users_activity')
    database = Database()
    connection = database.get_connection()

    def execute(self):
        try:
            log.info('ORSI0001', 'UsersActivity')
            user_ids = self.__get_target_user_ids()
            for __user_id in user_ids:
                user_id = __user_id['user_id']
                self.__set_users_activity(user_id)
            connection.commit()
            connection.close()
            log.info('ORSI0002', 'UsersActivity')
        except Exception as e:
            log.critical('ORSC0001', 'UsersActivity', e)
            raise Exception(e)

    def __get_target_user_ids(self):
        result = database.execute_statement(connection, 'm_users_003')
        user_ids = result[1]
        return user_ids

    def __set_users_activity(self, user_id):
        ripple_api = RippleApi()
        result = database.execute_statement(connection, 't_users_activity_S02', user_id)
        transact_scores = result[1]
        counter = 0
        for transact_score in transact_scores:
            leaderboard_scores = ripple_api.get_leaderboard(transact_score['beatmap_md5'], transact_score['play_mode'])
            leaderboard_scores = leaderboard_scores['scores']
            transact_score_score = transact_score['score']
            transact_score_score_id = transact_score['score_id']
            transact_score_user_id = transact_score['user_id']
            ranking = 1
            for leaderboard_score in leaderboard_scores:
                # Get score's ranking.
                leaderboard_score_score = leaderboard_score['score']
                leaderboard_score_score_id = leaderboard_score['id']
                leaderboard_score_user_id = leaderboard_score['user']['id']
                if leaderboard_score_score_id == transact_score_score_id:
                    break
                elif leaderboard_score_user_id == transact_score_user_id:
                    pass
                elif transact_score_score > leaderboard_score_score:
                    break
                else:
                    ranking = ranking + 1
            # Set users activity.
            beatmap_md5 = transact_score['beatmap_md5']
            result = database.execute_statement(connection, 't_users_activity_S03', beatmap_md5)
            activity_score = result[1][0]['score']
            if (activity_score == None or activity_score < transact_score['score']):
                result = database.execute_statement(connection, 'm_beatmaps_S02', beatmap_md5)
                beatmap_id = result[1][0]['beatmap_id']
                song_name = result[1][0]['song_name']
                activity = converter.convert_activity(transact_score, beatmap_id, song_name, ranking)
                result = database.execute_statement_values(connection, 't_users_activity_I01', activity.values())
                log.debug('ORSD0014', transact_score['user_id'], transact_score['score_id'], song_name, transact_score['score'], transact_score['rank'], ranking)
                # Mark the score has processed on transaction.
                result = database.execute_statement(connection, 'l_scores_on_activity_I01', user_id, transact_score_score_id, 1, transact_score['created_on'])
            else:
                # Mark the score has processed on transaction.
                result = database.execute_statement(connection, 'l_scores_on_activity_I01', user_id, transact_score_score_id, 3, transact_score['created_on'])
            counter = counter + 1
        log.info('ORSI0011',  counter, user_id)
