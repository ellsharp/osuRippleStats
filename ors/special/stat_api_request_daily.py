import sys
import os
from ors.script.database import Database
from ors.script import logger

if __name__ == "__main__":
    from ors.main.stat_api_request_daily import StatApiRequestDaily
    UsersActivity().execute()

class StatApiRequestDaily(object):
    global log
    global database
    global connection
    log = logger.logger('stat_api_request_daily')
    database = Database()
    connection = database.get_connection()

    def execute(self):
        process_name = 'StatApiRequestDaily'
        try:
            log.info('ORSI0001', process_name)
            self.__tally_api_request_daily()
            connection.commit()
            connection.close()
            log.info('ORSI0002', process_name)
        except Exception as e:
            log.critical('ORSC0001', process_name, e)
            raise Exception(e)

    def __tally_api_request_daily(self):
        result = database.execute_statement(connection, 's_api_request_daily_I01')
        result = database.execute_statement(connection, 's_api_request_tick_D01')
