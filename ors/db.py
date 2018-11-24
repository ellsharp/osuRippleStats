from ors.logger import logger
from ors import peppy_api
from ors import util
import traceback
import time
import pymysql
import sys
import os

logger = logger(str(os.path.basename(__file__)))

def get_database_connection():
    """
    Establish database connection and returns it.
    """
    # Read config file.
    config = util.get_config_object()

    # Get database parameters from config file.
    host = config['database']['host']
    db = config['database']['db']
    user = config['database']['user']
    password = config['database']['password']
    charset = config['database']['charset']

    # Try to get connection of database.
    try:
        logger.debug('Try to get database connection.')
        connection = pymysql.connect(
            host=host,
            db=db,
            user=user,
            password=password,
            charset=charset,
            cursorclass=pymysql.cursors.DictCursor
        )
        logger.debug('Try to get database connection has succeeded.')
    except Exception as e:
        logger.critical('Failed to get database connection. Exception[%s]\n %s' % (e, traceback.format_exc()))
        sys.exit(1)
    return connection

def close_database_connection(connection):
    """
    Close database connection and returns it.
    """
    try:
        logger.debug('Try to close database connection.')
        connection.close()
        logger.debug('Try to close database connection has succeeded.')
    except Exception as e:
        logger.error('Failed to close database connection. Exception[%s]\n %s' % (e, traceback.format_exc()))

def execute_delete_all_statement(connection, table_name):
    """
    Delete all record from table.
    Commit statement when succeeded and rollback it when failed.
    """
    # Read sql file.
    sql_file = open('sql/s_delete_all_from_table.sql', 'r')
    sql = sql_file.read()
    # Try to delete all record from table.
    try:
        logger.debug('Try to delete all record from table[%s]' % table_name)
        cursor = connection.cursor()
        count = cursor.execute(sql % (table_name))
        logger.info('Try to delete all record from table[%s] has succeeded. Count[%s]' % (table_name, count))
        connection.commit()
        cursor.close()
    except Exception as e:
        # When failed to commit statement, rollback table and system abnormal end.
        logger.critical('Failed to delete all record from table[%s]. Exception[%s]\n %s' % (table_name, e, traceback.format_exc()))
        logger.info('Rollback sql[%s] to table[%s]' % ('s_delete_all_from_table.sql', table_name))
        connection.rollback()
        sys.exit(1)

def execute_insert_statement_scores_work(connection, table_name, scores_data):
    """
    Insert user's scores data to work table.
    Commit statement when succeeded and rollback it when failed.
    """
    # Read sql file.
    sql_file = open('sql/s_insert_table.sql', 'r')
    sql = sql_file.read()
    # Try to delete all record from table.
    count = 0
    try:
        logger.debug('Try to insert record to table[%s]' % (table_name))
        cursor = connection.cursor()
        for score_data in scores_data:
            # Create statement.
            columns = ', '.join(score_data.keys())
            placeholders = ', '.join(['\'%s\''] * len(score_data))
            statement = (sql % (table_name, columns, placeholders))
            # Execute Statement
            cursor.execute(statement % tuple(score_data.values()))
            logger.debug('Try to insert score_id[%s] to table[%s] has succeeded.' % (score_data['score_id'], table_name))
            count = count + 1
        logger.info('Try to insert scores to table[%s] has succeeded. Count[%s]' % (table_name, count))
        connection.commit()
        cursor.close()
    except Exception as e:
        # When failed to commit statement, rollback table and system abnormal end.
        logger.critical('Failed to insert score_id[%s] from table[%s]. Exception[%s]\n %s' % (score_data['score_id'], table_name, e, traceback.format_exc()))
        logger.info('Rollback sql[%s] to table[%s]' % ('s_insert_table.sql', table_name))
        connection.rollback()
        sys.exit(1)

def execute_insert_statement_scores_transaction(connection, work_table_name, transaction_table_name):
    """
    Insert user's scores data to transaction table.
    Commit statement when succeeded and rollback it when failed.
    """
    cursor = connection.cursor()
    sql_file = open('sql/s_check_new_scores_transaction.sql', 'r')
    sql = sql_file.read()
    unregistered_score_ids = []
    try:
        logger.debug('Try to run sql[s_check_new_scores_transaction.sql].')
        cursor.execute(sql % (work_table_name, transaction_table_name))
        # Keep new score id.
        count = 0
        for score_id in cursor:
            unregistered_score_ids.append(score_id['score_id'])
            count = count + 1
        logger.info('Try to run sql[s_check_new_scores_transaction.sql] has suceeded. Count[%s].' % count)
    except Exception as e:
        logger.error('Failed to run sql[s_check_new_scores_transaction.sql]. Exception[%s]\n %s' % (e, traceback.format_exc()))
        connection.rollback()
        sys.exit(1)

    if (len(unregistered_score_ids) != 0):
        # Insert new scores to transaction table from work table.
        sql_file = open('sql/s_insert_to_transaction_from_work.sql', 'r')
        sql = sql_file.read()
        placeholders = ', '.join(['%s'] * len(unregistered_score_ids))
        for score_id in unregistered_score_ids:
            statement = (sql % (transaction_table_name, work_table_name, score_id))
            try:
                cursor.execute(statement)
                logger.debug('Try to insert score_id[%s] to table[%s] has succeeded.' % (score_id, transaction_table_name))
            except Exception as e:
                logger.error('Failed to insert score_id[%s] to table[%s]. Exception[%s]\n %s' % (tuple(unregistered_score_ids), transaction_table_name, e, traceback.format_exc()))
                logger.info('Rollback sql[%s] to table[%s]' % ('s_insert_to_transaction_from_work.sql', transaction_table_name))
                connection.rollback()
                sys.exit(1)
        connection.commit()
        cursor.close()
    else:
        logger.info('No unregistered scores are exists. Skips insert data from work to transaction.')

def execute_insert_statement_scores_master(connection, transaction_table_name, master_table_name):
    """
    Insert user's scores data to master table.
    Commit statement when succeeded and rollback it when failed.
    """
    cursor = connection.cursor()
    sql_file = open('sql/s_check_new_scores_master.sql', 'r')
    sql = sql_file.read()
    unregistered_score_ids = []
    try:
        logger.debug('Try to run sql[s_check_new_scores_master.sql].')
        cursor.execute(sql % (transaction_table_name, transaction_table_name, master_table_name))
        # Keep new score id.
        count = 0
        for score_id in cursor:
            unregistered_score_ids.append(score_id['score_id'])
            count = count + 1
        logger.info('Try to run sql[s_check_new_scores_master.sql] has suceeded. Count[%s]' % count)
    except Exception as e:
        logger.error('Failed to run sql[s_check_new_scores_master.sql]. Exception[%s]\n %s' % (e, traceback.format_exc()))
        connection.rollback()
        sys.exit(1)

    if (len(unregistered_score_ids) != 0):
        # Check the score is new or improved.
        new_score_ids = []
        improved_score_ids = []
        sql_file = open('sql/s_select_new_score_id.sql', 'r')
        sql = sql_file.read()
        for score_id in unregistered_score_ids:
            try:
                cursor.execute(sql % (master_table_name, transaction_table_name, score_id))
                count_fetch = cursor.fetchall()
                count = count_fetch[0]['count']
                if (count == 0):
                    new_score_ids.append(score_id)
                    logger.info('score_id[%s] is new score.' % score_id)
                else:
                    improved_score_ids.append(score_id)
                    logger.info('score_id[%s] is improved score.' % score_id)
                logger.debug('Try to run sql[s_select_new_score_id.sql] has suceeded.')
            except Exception as e:
                logger.error('Failed to run sql[s_select_new_score_id.sql]. Exception[%s]\n %s' % (e, traceback.format_exc()))
                connection.rollback()
                sys.exit(1)

        if(len(new_score_ids) != 0):
            # Insert new scores to master table from transaction table.
            for score_id in new_score_ids:
                sql_file = open('sql/s_insert_to_master_from_transaction.sql', 'r')
                sql = sql_file.read()
                statement = sql % (master_table_name, transaction_table_name, score_id)
                try:
                    cursor.execute(statement)
                    logger.info('Try to insert score_id[%s] to table[%s] has succeeded.' % (score_id, master_table_name))
                except Exception as e:
                    logger.error('Failed to insert score_id[%s] to table[%s]. Exception[%s]\n %s' % (score_id, master_table_name, e, traceback.format_exc()))
                    logger.info('Rollback sql[%s] to table[%s]' % ('s_insert_to_master_from_transaction.sql', master_table_name))
                    connection.rollback()
                    sys.exit(1)
                # Check is it first place ranks. # want merge it.
                sql_file = open('sql/s_select_beatmap_md5_from_score_id.sql', 'r')
                sql = sql_file.read()
                statement = sql % (master_table_name, score_id)
                try:
                    cursor.execute(statement)
                    data = cursor.fetchall()
                    beatmap_md5 = data[0]['beatmap_md5']
                    if (util.is_first_place_ranks('70666', beatmap_md5, 0)):
                        logger.info('score_id[%s] is first place.' % score_id)
                        sql_file = open('sql/s_insert_to_first_place.sql')
                        sql = sql_file.read()
                        statement = sql % ('m_first_place_std', master_table_name, score_id)
                        try:
                            cursor.execute(statement)
                        except Exception as e:
                            logger.error('Failed. Exception[%s]\n %s' % (e, traceback.format_exc()))
                            sys.exit(1)
                    else:
                        logger.info('score_id[%s] is not first place.' % score_id)
                except Exception as e:
                    logger.error('Failed. Exception[%s]\n %s' % (score_id, master_table_name, e, traceback.format_exc()))
                    sys.exit(1)

            connection.commit()
        else:
            logger.info('No new scores are exists. Skips insert score from transaction to master.')

        if(len(improved_score_ids) != 0):
            #Update improved scores to master table from transaction table.
            sql_file = open('sql/s_update_score_master.sql', 'r')
            sql = sql_file.read()
            for score_id in improved_score_ids:
                statement = (sql % (master_table_name, transaction_table_name, score_id, transaction_table_name, score_id))
                try:
                    cursor.execute(statement)
                    logger.info('Try to update score_id[%s] to table[%s] has succeeded.' % (score_id, master_table_name))
                except Exception as e:
                    logger.error('Failed to update score_id[%s] to table[%s]. Exception[%s]\n %s' % (score_id, master_table_name, e, traceback.format_exc()))
                    logger.info('Rollback sql[%s] to table[%s]' % ('s_update_score_master.sql', master_table_name))
                    connection.rollback()
                    cursor.close()
                    connection.close()
                    sys.exit(1)
                # Check is it first place ranks. # want merge it.
                sql_file = open('sql/s_select_beatmap_md5_from_score_id.sql', 'r')
                sql = sql_file.read()
                statement = sql % (master_table_name, score_id)
                try:
                    cursor.execute(statement)
                    data = cursor.fetchall()
                    beatmap_md5 = data[0]['beatmap_md5']
                    if (util.is_first_place_ranks(70666, beatmap_md5, 0)):
                        logger.info('score_id[%s] is first place.' % score_id)
                        sql_file = open('sql/s_insert_to_first_place.sql')
                        sql = sql_file.read()
                        statement = sql % ('m_first_place_std', master_table_name, score_id)
                        try:
                            cursor.execute(statement)
                        except Exception as e:
                            logger.error('Failed. Exception[%s]\n %s' % (e, traceback.format_exc()))
                            sys.exit(1)
                    else:
                        logger.info('score_id[%s] is not first place.' % score_id)
                except Exception as e:
                    logger.error('Failed. Exception[%s]\n %s' % (score_id, master_table_name, e, traceback.format_exc()))
                    sys.exit(1)
            connection.commit()
        else:
            logger.info('No improved scores are exists. Skips insert data from transaction to master.')
        return unregistered_score_ids
    else:
        logger.info('No unregistered scores are exists. Skips insert data from transaction to master.')

# -------------------------------user stats------------------------------------
def execute_insert_statement_stats_work(connection, table_name, stats_data):
    """
    Insert user's stats data to work table.
    Commit statement when succeeded and rollback it when failed.
    """
    # Read sql file.
    sql_file = open('sql/s_insert_table.sql', 'r')
    sql = sql_file.read()
    # Try to delete all record from table.
    try:
        logger.debug('Try to insert record to table[%s]' % (table_name))
        cursor = connection.cursor()
        columns = ', '.join(stats_data.keys())
        placeholders = ', '.join(['\'%s\''] * len(stats_data))
        statement = (sql % (table_name, columns, placeholders))
        # Execute Statement
        cursor.execute(statement % tuple(stats_data.values()))
        logger.debug('Try to insert user_id[%s] to table[%s] has succeeded.' % (stats_data['user_id'], table_name))

        logger.info('Try to insert stats user_id[%s] to table[%s] has succeeded.' % (stats_data['user_id'], table_name))
        connection.commit()
        cursor.close()
    except Exception as e:
        # When failed to commit statement, rollback table and system abnormal end.
        logger.critical('Failed to insert user_id[%s] from table[%s]. Exception[%s]\n %s' % (stats_data['user_id'], table_name, e, traceback.format_exc()))
        logger.info('Rollback sql[%s] to table[%s]' % ('s_insert_table.sql', table_name))
        connection.rollback()
        sys.exit(1)

def execute_insert_statement_stats_transaction(connection, user_id, work_table_name, transaction_table_name):
    """
    Insert user's stats data to transaction table.
    Commit statement when succeeded and rollback it when failed.
    """
    # Read sql file.
    sql_file = open('sql/s_insert_stats_to_transaction_from_work.sql', 'r')
    sql = sql_file.read()
    # Try to delete all record from table.
    try:
        logger.debug('Try to insert user_id[%s] stats to table[%s]' % (user_id, transaction_table_name))
        cursor = connection.cursor()
        statement = (sql % (transaction_table_name, work_table_name, user_id))
        # Execute Statement
        cursor.execute(statement)
        logger.info('Try to insert stats user_id[%s] to table[%s] has succeeded.' % (user_id, transaction_table_name))
        connection.commit()
        cursor.close()
    except Exception as e:
        # When failed to commit statement, rollback table and system abnormal end.
        logger.critical('Failed to insert user_id[%s] from table[%s]. Exception[%s]\n %s' % (user_id, transaction_table_name, e, traceback.format_exc()))
        logger.info('Rollback sql[%s] to table[%s]' % ('s_insert_table.sql', transaction_table_name))
        connection.rollback()
        sys.exit(1)

def execute_insert_statement_stats_master(connection, user_id, transaction_table_name, master_table_name):
    """
    Update user's stats data to master table.
    Commit statement when succeeded and rollback it when failed.
    """
    cursor = connection.cursor()
    sql_file = open('sql/s_count_user_id_in_master.sql', 'r')
    sql = sql_file.read()
    is_newbie = True
    try:
        cursor.execute(sql % (master_table_name, user_id))
        count_fetch = cursor.fetchall()
        count = count_fetch[0]['count']
        if (count != 0):
            is_newbie = False
            logger.info('user_id[%s] is already exists in table[%s].' % (user_id, master_table_name))
        else:
            logger.info('user_id[%s] is not exists in table[%s].' % (user_id, master_table_name))
        logger.debug('Try to run sql[s_count_user_id_in_master.sql] has suceeded.')
    except Exception as e:
        logger.error('Failed to run sql[s_count_user_id_in_master.sql]. Exception[%s]\n %s' % (e, traceback.format_exc()))
        connection.rollback()
        sys.exit(1)

    if(is_newbie):
        # Insert new user's stats to master table from transaction table.
        sql_file = open('sql/s_insert_stats_to_master_from_transaction.sql', 'r')
        sql = sql_file.read()
        statement = (sql % (master_table_name, transaction_table_name, user_id))
        try:
            cursor.execute(statement)
            logger.info('Try to insert user_id[%s] to table[%s] has succeeded.' % (user_id, master_table_name))
        except Exception as e:
            logger.error('Failed to insert user_id[%s] to table[%s]. Exception[%s]\n %s' % (user_id, master_table_name, e, traceback.format_exc()))
            logger.info('Rollback sql[%s] to table[%s]' % ('s_insert_stats_to_master_from_transaction.sql', master_table_name))
            connection.rollback()
            sys.exit(1)
    else:
        # Update exixts user's stats to master table from transaction table.
        sql_file = open('sql/s_update_stats_master.sql', 'r')
        sql = sql_file.read()
        statement = (sql % (master_table_name, transaction_table_name, transaction_table_name, user_id))
        try:
            cursor.execute(statement)
            logger.info('Try to update stats user_id[%s] to table[%s] has succeeded.' % (user_id, master_table_name))
        except Exception as e:
            logger.error('Failed to insert user_id[%s] to table[%s]. Exception[%s]\n %s' % (user_id, master_table_name, e, traceback.format_exc()))
            logger.info('Rollback sql[%s] to table[%s]' % ('s_update_stats_master.sql', master_table_name))
            connection.rollback()
            sys.exit(1)
    connection.commit()

def execute_update_beatmap_master_temp(connection, beatmap_data, beatmaps_table_name):
    """
    Update beatmap data of master.
    Commit statement when succeeded and rollback it when failed.
    """
    beatmap_md5 = beatmap_data[0]['file_md5']
    cursor = connection.cursor()
    sql_file = open('sql/s_check_beatmap_data_exists.sql', 'r')
    sql = sql_file.read()
    is_new_beatmap = True
    try:
        cursor.execute(sql % (beatmaps_table_name, beatmap_md5))
        count_fetch = cursor.fetchall()
        count = count_fetch[0]['count']
        if (count != 0):
            is_new_beatmap = False
            logger.info('beatmap_md5[%s] is already exists in table[%s].' % (beatmap_md5, beatmaps_table_name))
        else:
            logger.info('beatmap_md5[%s] is not exists in table[%s].' % (beatmap_md5, beatmaps_table_name))
        logger.debug('Try to run sql[s_check_beatmap_data_exists.sql] has suceeded.')
    except Exception as e:
        logger.error('Failed to run sql[s_check_beatmap_data_exists.sql]. Exception[%s]\n %s' % (e, traceback.format_exc()))
        connection.rollback()
        sys.exit(1)

    beatmap_data = dict(beatmap_data[0])
    if(is_new_beatmap):
        # Insert new beatmap data to master table.
        sql_file = open('sql/s_insert_table.sql', 'r')
        sql = sql_file.read()
        columns = ', '.join(beatmap_data.keys())
        placeholders = ', '.join(['\"%s\"'] * len(beatmap_data))
        statement = (sql % (beatmaps_table_name, columns, placeholders))
        try:
            cursor.execute(statement % tuple(beatmap_data.values()))
            connection.commit()
            cursor.close()
            logger.info('Try to insert beatmap_md5[%s] to table[%s] has succeeded.' % (beatmap_md5, beatmaps_table_name))
        except Exception as e:
            logger.error('Failed to insert beatmap_md5[%s] to table[%s]. Exception[%s]\n %s' % (beatmap_md5, beatmaps_table_name, e, traceback.format_exc()))
            logger.info('Rollback sql[%s] to table[%s]' % ('s_insert_table.sql', beatmaps_table_name))
            connection.rollback()
            sys.exit(1)

def execute_update_beatmap_master(connection, inserted_score_ids, master_table_name, beatmaps_table_name):
    """
    Update beatmap data of master.
    Commit statement when succeeded and rollback it when failed.
    """
    # Get beatmap_md5.
    beatmap_md5s = []
    cursor = connection.cursor()
    sql_file = open('sql/s_select_beatmap_md5_from_score_id.sql', 'r')
    sql = sql_file.read()
    for score_id in inserted_score_ids:
        try:
            cursor.execute(sql % (master_table_name, score_id))
            beatmap_md5_fetch = cursor.fetchall()
            beatmap_md5 = beatmap_md5_fetch[0]['beatmap_md5']
            beatmap_md5s.append(beatmap_md5)
        except Exception as e:
            logger.error('Failed to run sql[s_select_beatmap_md5_from_score_id.sql]. Exception[%s]\n %s' % (e, traceback.format_exc()))
            connection.rollback()
            sys.exit(1)
    # Check beatmap data exists on m_beatmap table.
    sql_file = open('sql/s_check_beatmap_data_exists.sql', 'r')
    sql = sql_file.read()
    new_beatmap_md5s = []
    for beatmap_md5 in beatmap_md5s:
        try:
            cursor.execute(sql % (beatmaps_table_name, beatmap_md5))
            count_fetch = cursor.fetchall()
            count = count_fetch[0]['count']
            if (count != 0):
                logger.info('beatmap_md5[%s] is already exists in table[%s].' % (beatmap_md5, beatmaps_table_name))
            else:
                new_beatmap_md5s.append(beatmap_md5)
                logger.info('beatmap_md5[%s] is not exists in table[%s].' % (beatmap_md5, beatmaps_table_name))
            logger.debug('Try to run sql[s_check_beatmap_data_exists.sql] has suceeded.')
        except Exception as e:
            logger.error('Failed to run sql[s_check_beatmap_data_exists.sql]. Exception[%s]\n %s' % (e, traceback.format_exc()))
            connection.rollback()
            sys.exit(1)
    # Access to peppy api and get beatmap data.
    for beatmap_md5 in new_beatmap_md5s:
        beatmap_data = peppy_api.get_beatmaps(beatmap_md5, 0, 0, 1)
        if beatmap_data == None:
            continue;
        beatmap_data = dict(beatmap_data[0])
        beatmap_data = util.convert_beatmap_data(beatmap_data)
        # Insert new beatmap data to master table.
        sql_file = open('sql/s_insert_table.sql', 'r')
        sql = sql_file.read()
        columns = ', '.join(beatmap_data.keys())
        placeholders = ', '.join(['\"%s\"'] * len(beatmap_data))
        statement = (sql % (beatmaps_table_name, columns, placeholders))
        try:
            cursor.execute(statement % tuple(beatmap_data.values()))
            connection.commit()
            logger.info('Try to insert beatmap_md5[%s] to table[%s] has succeeded.' % (beatmap_md5, beatmaps_table_name))
        except Exception as e:
            logger.error('Failed to insert beatmap_md5[%s] to table[%s]. Exception[%s]\n %s' % (beatmap_md5, beatmaps_table_name, e, traceback.format_exc()))
            logger.info('Rollback sql[%s] to table[%s]' % ('s_insert_table.sql', beatmaps_table_name))
            connection.rollback()
            sys.exit(1)

def execute_update_all_beatmap_master(connection, master_table_name, beatmaps_table_name):
    """
    Update all beatmap data of master.
    Commit statement when succeeded and rollback it when failed.
    """
    cursor = connection.cursor()
    sql_file = open('sql/s_select_unregister_beatmap.sql', 'r')
    sql = sql_file.read()
    unregistered_beatmap_md5s = []
    try:
        cursor.execute(sql % (master_table_name, beatmaps_table_name))
        unregistered_beatmap_md5s = cursor.fetchall()
        logger.info('Try to check unregisterd beatmap data has succeeded.')
    except Exception as e:
        logger.error('Failed to check unregisterd beatmap data. Exception[%s]\n %s' % (e, traceback.format_exc()))
        sys.exit(1)
    print('Unregistered beatmap number: %s' % str(len(unregistered_beatmap_md5s)))
    exception_beatmap_md5 = []
    for data in unregistered_beatmap_md5s:
        # Access to peppy api and get beatmap data.
        beatmap_md5 = data['beatmap_md5']
        beatmap_data = peppy_api.get_beatmaps(beatmap_md5, 0, 0, 1)
        try:
            beatmap_data = dict(beatmap_data[0])
        except Exception as e:
            exception_beatmap_md5.append(beatmap_md5)
            logger.debug('beatmap_md5[%s] could not get beatmap data. API response[%s]' % (beatmap_md5, beatmap_data))
            continue
        beatmap_data = util.convert_beatmap_data(beatmap_data)
        # Insert new beatmap data to master table.
        sql_file = open('sql/s_insert_table.sql', 'r')
        sql = sql_file.read()
        columns = ', '.join(beatmap_data.keys())
        placeholders = ', '.join(['\"%s\"'] * len(beatmap_data))
        statement = (sql % (beatmaps_table_name, columns, placeholders))
        print(beatmap_md5)
        try:
            cursor.execute(statement % tuple(beatmap_data.values()))
            connection.commit()
            logger.info('Try to insert beatmap_md5[%s] to table[%s] has succeeded.' % (beatmap_md5, beatmaps_table_name))
        except Exception as e:
            logger.error('Failed to insert beatmap_md5[%s] to table[%s]. Exception[%s]\n %s' % (beatmap_md5, beatmaps_table_name, e, traceback.format_exc()))
            logger.info('Rollback sql[%s] to table[%s]' % ('s_insert_table.sql', beatmaps_table_name))
            connection.rollback()
            sys.exit(1)
        time.sleep(1)

def execute_update_all_first_place_master(connection, master_table_name, first_place_table_name):
    """
    Update all first place data of master.
    Commit statement when succeeded and rollback it when failed.
    """
    cursor = connection.cursor()
    sql_file = open('sql/s_select_all_beatmap_md5.sql', 'r')
    sql = sql_file.read()
    beatmap_md5s = []
    try:
        cursor.execute(sql % (master_table_name, 70666))
        beatmap_md5s = cursor.fetchall()
        logger.info('Try to select all beatmap_md5 has succeeded.')
    except Exception as e:
        logger.error('Failed to select all beatmap_md5. Exception[%s]\n %s' % (e, traceback.format_exc()))
        sys.exit(1)
    # Check the first place.
    for beatmap_md5 in beatmap_md5s:
        beatmap_md5 = beatmap_md5['beatmap_md5']
        if (util.is_first_place_ranks(70666, beatmap_md5, 0)):
            sql_file = open('sql/s_insert_to_first_place_with_beatmap_md5.sql', 'r')
            sql = sql_file.read()
            statement = sql % (first_place_table_name, master_table_name, beatmap_md5)
            try:
                print(statement)
                cursor.execute(statement)
                logger.debug('Insert beatmap_md5[%s] succeeded.' % beatmap_md5)
            except Exception as e:
                logger.error('Failed to insert. Exception[%s]\n %s' % (e, traceback.format_exc()))
                sys.exit(1)
    connection.commit()
    cursor.close()
