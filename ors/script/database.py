import re
import sys
import pymysql
from ors.script import util
from ors.script import logger

if __name__ == "__main__":
    from ors.script import Database
    Database().execute()

class Database(object):
    global log
    log = logger.logger('database')

    def get_connection(self):
        config = util.read_config()
        host = config['database']['host']
        db = config['database']['db']
        user = config['database']['user']
        password = config['database']['password']
        charset = config['database']['charset']
        try:
            connection = pymysql.connect(
                host=host,
                db=db,
                user=user,
                password=password,
                charset=charset,
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            log.critical('ORSC0003', e)
            sys.exit(1)
        return connection

    def execute_statement(self, connection, sql_name, *parameters):
        sql_path = 'sql/' + sql_name + '.sql'
        sql_file = open(sql_path, 'r')
        sql = sql_file.read()
        statement = sql % parameters
        try:
            cursor = connection.cursor()
            count = cursor.execute(statement)
            result = cursor.fetchall()
            cursor.close()
        except Exception as e:
            # When failed to commit statement, rollback table and system abnormal end.
            connection.rollback()
            log.critical('ORSC0004', 'execute_statement', e, sql_name, self.__compress_statement(statement))
            sys.exit(1)
        return [count, result]

    def execute_statement_values(self, connection, sql_name, values):
        sql_path = 'sql/' + sql_name + '.sql'
        sql_file = open(sql_path, 'r')
        sql = sql_file.read()
        statement = sql % tuple(values)
        try:
            cursor = connection.cursor()
            count = cursor.execute(statement)
            result = cursor.fetchall()
            cursor.close()
        except Exception as e:
            # When failed to commit statement, rollback table and system abnormal end.
            connection.rollback()
            log.critical('ORSC0004', 'execute_statement_values', e, sql_name, self.__compress_statement(statement))
            sys.exit(1)
        return [count, result]

    def __compress_statement(self, statement):
        statement = re.sub(r"\s+", " ", statement)
        return statement
