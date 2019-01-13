import sys
import os
from ors.script.database import Database
from ors.script.ripple_api import RippleApi
from ors.script import converter
from ors.script import logger

if __name__ == "__main__":
    from ors.main.first_place_master import FirstPlaceMaster
    FirstPlaceMaster().execute()

class FirstPlaceMaster(object):
    global log
    global database
    global connection
    log = logger.logger('first_place_master')
    database = Database()
    connection = database.get_connection()

    def execute(self):
        try:
            log.info('ORSI0001', 'FirstPlaceMaster')
            user_ids = self.__get_target_user_ids()
            for __user_id in user_ids:
                user_id = __user_id['user_id']
                self.__check_first_place(user_id)
                self.__set_first_place(user_id)
            connection.commit()
            connection.close()
            log.info('ORSI0002', 'FirstPlaceMaster')
        except Exception as e:
            log.critical('ORSC0001', 'FirstPlaceMaster', e)
            raise Exception(e)

    def __get_target_user_ids(self):
        result = database.execute_statement(connection, 'm_users_003')
        user_ids = result[1]
        return user_ids

    def __check_first_place(self, user_id):
        ripple_api = RippleApi()
        result = database.execute_statement(connection, 'm_first_place_S02', user_id)
        log.info('ORSI0011', result[0], user_id)
        first_place_scores = result[1]
        not_changed_counter = 0
        lost_counter = 0
        for first_place_score in first_place_scores:
            beatmap_md5 = first_place_score['beatmap_md5']
            mode = first_place_score['play_mode']
            leaderboard_scores = ripple_api.get_leaderboard(beatmap_md5, mode)
            first_place_now_score_id = leaderboard_scores['scores'][0]['id']
            # NEED TEST HERE.
            if first_place_now_score_id != first_place_score['score_id']:
                # The case lost first place.
                result = database.execute_statement(connection, 'm_beatmaps_S02', beatmap_md5)
                beatmap_id = result[1][0]['beatmap_id']
                song_name = result[1][0]['song_name']
                del first_place_score['time']
                first_place_score['time'] = leaderboard_scores['scores'][0]['time']
                first_place_score = converter.convert_first_place_score(first_place_score)
                activity = converter.convert_activity(first_place_score, beatmap_id, song_name, -1)
                result = database.execute_statement_values(connection, 't_users_activity_I01', activity.values())
                result = database.execute_statement(connection, 'm_first_place_D01', first_place_score['score_id'])
                log.debug('ORSD0017', user_id, first_place_score['score_id'], song_name, first_place_score['score'], first_place_score['rank'])
                lost_counter = lost_counter + 1
            else:
                result = database.execute_statement(connection, 'm_beatmaps_S02', beatmap_md5)
                song_name = result[1][0]['song_name']
                log.debug('ORSD0018', user_id, first_place_score['score_id'], song_name, first_place_score['score'], first_place_score['rank'])
                not_changed_counter = not_changed_counter + 1
        log.info('ORSI0013', user_id, not_changed_counter, lost_counter)

    def __set_first_place(self, user_id):
        result = database.execute_statement(connection, 't_users_activity_S04', user_id)
        activity_score_infos = result[1]
        for activity_score_info in activity_score_infos:
            activity_score_id = activity_score_info['score_id']
            activity_beatmap_md5 = activity_score_info['beatmap_md5']
            # Check updated score.
            result = database.execute_statement(connection, 'm_first_place_S01', activity_beatmap_md5)
            count = result[0]
            if count == 0:
                result = database.execute_statement(connection, 't_users_scores_S02', activity_score_id)
                score = result[1][0]
                del score['updated_on']
                result = database.execute_statement_values(connection, 'm_first_place_I01', score.values())
                result = database.execute_statement(connection, 'l_scores_on_first_place_I01', user_id, score['score_id'], 1, score['created_on'])
                result = database.execute_statement(connection, 'm_beatmaps_S01', score['beatmap_md5'])
                song_name = result[1][0]['song_name']
                log.debug('ORSD0015', user_id, activity_score_id, song_name, score['score'], score['rank'])
            else:
                if activity_score_id != result[1][0]['score_id']:
                    result = database.execute_statement(connection, 't_users_scores_S02', activity_score_id)
                    score = result[1][0]
                    created_on = score['created_on']
                    del score['created_on']
                    del score['updated_on']
                    score.update(beatmap_md5_key=score['beatmap_md5'])
                    result = database.execute_statement_values(connection, 'm_first_place_U01', score.values())
                    result = database.execute_statement(connection, 'l_scores_on_first_place_I01', user_id, score['score_id'], 2, created_on)
                    result = database.execute_statement(connection, 'm_beatmaps_S01', score['beatmap_md5'])
                    song_name = result[1][0]['song_name']
                    log.debug('ORSD0016', user_id, activity_score_id, song_name, score['score'], score['rank'])
                else:
                    result = database.execute_statement(connection, 'l_scores_on_first_place_I01', user_id, score['score_id'], 3, created_on)
