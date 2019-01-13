import traceback
import sys
import os
from ors.script.database import Database
from ors.script.ripple_api import RippleApi
from ors.script import converter
from ors.script import logger
from ors.script import util

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
        try:
            log.info('ORSI0001', 'UsersScoresMaster')
            user_ids = self.__get_target_user_ids()
            for __user_id in user_ids:
                user_id = __user_id['user_id']
                new_scores = self.__get_users_scores_transaction(user_id)
                self.__set_users_scores_master(new_scores, user_id)
            connection.commit()
            connection.close()
            log.info('ORSI0002', 'UsersScoresMaster')
        except Exception as e:
            log.critical('ORSC0001', 'UsersScoreMaster', e)
            raise Exception(e)

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
                del new_score['updated_on']
                result = database.execute_statement_values(connection, 'm_users_scores_I01', new_score.values())
                beatmap_info = util.get_beatmap_info(new_score['beatmap_md5'], new_score['play_mode'])
                song_name = beatmap_info['song_name']
                log.debug('ORSD0011', new_score['user_id'], new_score['score_id'], song_name, new_score['score'], new_score['rank'])
                # Mark the score has processed on transaction.
                result = database.execute_statement(connection, 'l_scores_on_master_I01', user_id, new_score['score_id'], 1, new_score['created_on'])
                new_counter = new_counter + 1
            else:
                # Case of updated or not score.
                master_score = master_score[0]
                master_scores_score = master_score['score']
                new_scores_score = new_score['score']
                if new_scores_score > master_scores_score:
                    # Case of updated score.
                    created_on = new_score['created_on']
                    del new_score['created_on']
                    del new_score['updated_on']
                    new_score.update(beatmap_md5_key=new_score['beatmap_md5'])
                    result = database.execute_statement_values(connection, 'm_users_scores_U01', new_score.values())
                    beatmap_info = util.get_beatmap_info(new_score['beatmap_md5'], new_score['play_mode'])
                    song_name = beatmap_info['song_name']
                    log.debug('ORSD0012', new_score['user_id'], new_score['score_id'], song_name, new_score['score'], new_score['rank'])
                    # Mark the score has processed on transaction.
                    result = database.execute_statement(connection, 'l_scores_on_master_I01', user_id, new_score['score_id'], 2, created_on)
                    updated_counter = updated_counter + 1
                else:
                    # Case of not updated score.
                    beatmap_info = util.get_beatmap_info(new_score['beatmap_md5'], new_score['play_mode'])
                    song_name = beatmap_info['song_name']
                    log.debug('ORSD0013', new_score['user_id'], new_score['score_id'], song_name, new_score['score'], new_score['rank'])
                    # Mark the score has processed on transaction.
                    result = database.execute_statement(connection, 'l_scores_on_master_I01', user_id, new_score['score_id'], 3, new_score['created_on'])
                    not_updated_counter = not_updated_counter + 1;
        log.info('ORSI0010', new_counter, updated_counter, not_updated_counter)
