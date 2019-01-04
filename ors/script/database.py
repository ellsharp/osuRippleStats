import re
import sys
import pymysql
from ors.script import util
from ors.script import logger
log = logger.logger('Database')

def get_connection():
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
        print(e)
        sys.exit(1)
    return connection

def execute_statement(sql_name, *parameters):
    global log
    sql_path = 'sql/' + sql_name + '.sql'
    sql_file = open(sql_path, 'r')
    sql = sql_file.read()
    statement = sql % parameters
    log.debug('ORSD0004', compress_statement(statement))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        count = cursor.execute(statement)
        result = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        # When failed to commit statement, rollback table and system abnormal end.
        connection.rollback()
        log.critical('ORSC0001', 'execute_statement', e)
        sys.exit(1)
    return [count, result]

def execute_statement_values(sql_name, values):
    global log
    sql_path = 'sql/' + sql_name + '.sql'
    sql_file = open(sql_path, 'r')
    sql = sql_file.read()
    statement = sql % tuple(values)
    log.debug('ORSD0004', compress_statement(statement))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        count = cursor.execute(statement)
        result = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        # When failed to commit statement, rollback table and system abnormal end.
        connection.rollback()
        log.critical('ORSC0001', 'execute_statement', e)
        sys.exit(1)
    return [count, result]

def compress_statement(statement):
    statement = re.sub(r"\s+", " ", statement)
    return statement
