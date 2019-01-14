import sys
import os
from ors.script.database import Database
from ors.script import converter
from ors.script import logger
from ors.script import util

if __name__ == "__main__":
    from ors.main.users_stats_monthly import UsersStatsMonthly
    UsersStatsMonthly().execute()

class UsersStatsMonthly(object):
    global log
    global database
    global connection
    log = logger.logger('users_stats_monthly')
    database = Database()
    connection = database.get_connection()

    def execute(self):
        process_name = 'UsersStatsMonthly'
        try:
            log.info('ORSI0001', process_name)
            user_ids = self.__get_target_user_ids()
            for __user_id in user_ids:
                user_id = __user_id['user_id']
                self.__set_users_stats_monthly(user_id)
            connection.commit()
            connection.close()
            log.info('ORSI0002', process_name)
        except Exception as e:
            log.critical('ORSC0001', process_name, e)
            raise Exception(e)

    def __get_target_user_ids(self):
        result = database.execute_statement(connection, 'm_users_003')
        user_ids = result[1]
        return user_ids

    def __set_users_stats_monthly(self, user_id):
        process_month = util.datetime_now().strftime('%Y-%m')
        # Get how long stats are exists on transaction table.
        result = database.execute_statement(connection, 't_users_stats_S02', user_id)
        if (result[0] < 2):
            pass
        else:
            months = result[1];
            for month in months:
                month = month['created_on']
                result = database.execute_statement(connection, 't_users_stats_monthly_S01', month, user_id)
                count = result[1][0]['count']
                if (count == 1 and process_month != month) :
                    pass
                else:
                    result = database.execute_statement(connection, 't_users_stats_monthly_S02', month, user_id, user_id)
                    month_latest_stats = result[1][0]
                    result = database.execute_statement(connection, 't_users_stats_monthly_S03', month, user_id, user_id)
                    month_oldest_stats = result[1][0]
                    monthly_stats = converter.convert_monthly_stats(month, month_latest_stats, month_oldest_stats)
                    if (count == 0):
                        result = database.execute_statement_values(connection, 't_users_stats_monthly_I01', monthly_stats.values())
                    elif (count == 1 and process_month == month):
                        del monthly_stats['created_on']
                        monthly_stats.update(user_id_key=user_id)
                        monthly_stats.update(month_key=month)
                        result = database.execute_statement_values(connection, 't_users_stats_monthly_U01', monthly_stats.values())
