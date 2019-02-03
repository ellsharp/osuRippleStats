import sys
import os
from ors.script.database import Database
from ors.script import converter
from ors.script import logger

if __name__ == "__main__":
    from ors.main.users_stats_master import UsersStatsMaster
    UsersStatsMaster().execute()

class UsersStatsMaster(object):
    global log
    global database
    global connection
    log = logger.logger('users_stats_master')
    database = Database()
    connection = database.get_connection()

    def execute(self):
        try:
            log.info('ORSI0001', 'UsersStatsMaster')
            user_ids = self.__get_target_user_ids()
            for __user_id in user_ids:
                user_id = __user_id['user_id']
                latest_stats = self.__get_users_latest_stats(user_id)
                self.__set_users_stats_master(latest_stats, user_id)
                self.__set_users_badges_master(user_id)
                #self.__set_users_silence_info_master(user_id)
            connection.commit()
            connection.close()
            log.info('ORSI0002', 'UsersStatsMaster')
        except Exception as e:
            log.critical('ORSC0001', 'UsersStatsMaster', e)
            raise Exception(e)

    def __get_target_user_ids(self):
        result = database.execute_statement(connection, 'm_users_003')
        user_ids = result[1]
        return user_ids

    def __get_users_latest_stats(self, user_id):
        result = database.execute_statement(connection, 't_users_stats_S01', user_id)
        users_latest_stats = result[1]
        return users_latest_stats

    def __set_users_stats_master(self, latest_stats, user_id):
        result = database.execute_statement(connection, 'm_users_stats_S01', user_id)
        count = result[1][0]['count']
        latest_stats = latest_stats[0]
        if count == 0:
            log.info('ORSI0006', latest_stats['user_id'], latest_stats['username'])
            del latest_stats['updated_on']
            result = database.execute_statement_values(connection, 'm_users_stats_I01', latest_stats.values())
            log.debug('ORSD0002', 'm_users_stats', result[0], user_id)
        else:
            log.info('ORSI0007', latest_stats['user_id'], latest_stats['username'])
            del latest_stats['created_on']
            del latest_stats['updated_on']
            latest_stats.update(user_id_key=latest_stats['user_id'])
            result = database.execute_statement_values(connection, 'm_users_stats_U01', latest_stats.values())
            log.debug('ORSD0007', 'm_users_stats', result[0], user_id)

    def __set_users_badges_master(self, user_id):
        # Get latest users badges.
        result = database.execute_statement(connection, 't_users_badges_S01', user_id)
        users_badges = result[1]
        # Check users badges records are exists on master table.
        result = database.execute_statement(connection, 'm_users_badges_S01', user_id)
        count = result[1][0]['count']
        if count == 0:
            # If count is 0, there are no records on master table.
            # So create new record with insert statement.
            for users_badge in users_badges:
                del users_badge['updated_on']
                result = database.execute_statement_values(connection, 'm_users_badges_I01', users_badge.values())
        else:
            # If count is not 0, there are records on master table.
            # So update exists records with update statement.
            for users_badge in users_badges:
                del users_badge['created_on']
                del users_badge['updated_on']
                users_badge.update(user_id_key=users_badge['user_id'])
                users_badge.update(badge_id_key=users_badge['badge_id'])
                result = database.execute_statement_values(connection, 'm_users_badges_U01', users_badge.values())
