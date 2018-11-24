import traceback
import requests
import pymysql
import sys
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from PIL import Image
from ors import db
from ors import util
from ors import core
from ors import ripple_api
from ors.logger import logger
from datetime import datetime
from datetime import timezone

logger = logger(str(os.path.basename(__file__)))


def update_users_stats_work(user_id, mode):
    """
    Insert user's scores to work table.
    """
    # Read config file.
    config = util.get_config_object()
    # Read ripple api token key.
    ripple_token = config['token']['X-Ripple-Token']
    # Get user's recent stats from ripple api.
    users_stats_full = ripple_api.get_users_full(ripple_token, user_id)
    # Convert user's stats data to format of database.
    users_stats = util.convert_stats_data(user_id, users_stats_full, mode)
    # Define work table name.
    work_table_name = util.get_users_stats_work_table_name(mode)
    # Establish to database and get connection.
    connection = db.get_database_connection()
    # Delete all data of user's scores work table.
    db.execute_delete_all_statement(connection, work_table_name)
    # Insert user's scores data to work table.
    db.execute_insert_statement_stats_work(connection, work_table_name, users_stats)
    # Close database connection
    db.close_database_connection(connection)

def update_users_stats_transaction(user_id, mode):
    """
    Insert user's stats to transaction table.
    """
    # Define work table name.
    work_table_name = util.get_users_stats_work_table_name(mode)
    # Define transaction table name.
    transaction_table_name = util.get_users_stats_transaction_table_name(mode)
    # Establish to database and get connection.
    connection = db.get_database_connection()
    # Insert user's scores data to transaction table.
    db.execute_insert_statement_stats_transaction(connection, user_id, work_table_name, transaction_table_name)
    # Close database connection
    db.close_database_connection(connection)

def update_users_stats_master(user_id, mode):
    """
    Insert user's stats to master table.
    """
    # Define transaction table name.
    transaction_table_name = util.get_users_stats_transaction_table_name(mode)
    # Define master table name.
    master_table_name = util.get_users_stats_master_table_name(mode)
    # Establish to database and get connection.
    connection = db.get_database_connection()
    # Insert user's scores data to transaction table.
    db.execute_insert_statement_stats_master(connection, user_id, transaction_table_name, master_table_name)
    # Close database connection
    db.close_database_connection(connection)

def update_users_scores_work(user_id, mode):
    """
    Insert user's scores to work table.
    """
    # Read config file.
    config = util.get_config_object()
    # Read ripple api token key.
    ripple_token = config['token']['X-Ripple-Token']
    # Get user's recent scores from ripple api.
    users_scores_recent = ripple_api.get_users_scores_recent(ripple_token, user_id, mode,  100)
    # Convert user's scores data to format of database.
    users_scores = util.convert_scores_data(user_id, users_scores_recent)
    # Define work table name.
    work_table_name = util.get_users_scores_work_table_name(mode)
    # Establish to database and get connection.
    connection = db.get_database_connection()
    # Delete all data of user's scores work table.
    db.execute_delete_all_statement(connection, work_table_name)
    # Insert user's scores data to work table.
    db.execute_insert_statement_scores_work(connection, work_table_name, users_scores)
    # Close database connection
    db.close_database_connection(connection)

def update_users_scores_transaction(user_id, mode):
    """
    Insert user's scores to transaction table.
    """
    # Define work table name.
    work_table_name = util.get_users_scores_work_table_name(mode)
    # Define transaction table name.
    transaction_table_name = util.get_users_scores_transaction_table_name(mode)
    # Establish to database and get connection.
    connection = db.get_database_connection()
    # Insert user's scores data to transaction table.
    db.execute_insert_statement_scores_transaction(connection, work_table_name, transaction_table_name)
    # Close database connection
    db.close_database_connection(connection)

def update_users_scores_master(user_id, mode):
    """
    Insert user's scores to master table.
    """
    # Define transaction table name.
    transaction_table_name = util.get_users_scores_transaction_table_name(mode)
    # Define users score master table name.
    master_table_name = util.get_users_scores_master_table_name(mode)
    # Define beatmaps master table name.
    beatmaps_table_name = util.get_beatmaps_table_name(mode)
    # Establish to database and get connection.
    connection = db.get_database_connection()
    # Insert user's scores data to transaction table.
    inserted_score_ids = db.execute_insert_statement_scores_master(connection, transaction_table_name, master_table_name)
    # Update beatmaps data master.
    if (inserted_score_ids != None):
        db.execute_update_beatmap_master(connection, inserted_score_ids, master_table_name, beatmaps_table_name)
    # Close database connection
    db.close_database_connection(connection)

def update_all_beatmap_master(mode):
    """
    Update all beatmap data to master table.
    """
    # Define users score master table name.
    master_table_name = util.get_users_scores_master_table_name(mode)
    # Define beatmap master table name.
    beatmaps_table_name = util.get_beatmaps_table_name(mode)
    # Establish to database and get connection.
    connection = db.get_database_connection()
    # Insert user's scores data to master table.
    db.execute_update_all_beatmap_master(connection, master_table_name, beatmaps_table_name)
    # Close database connection
    db.close_database_connection(connection)

def update_all_first_place_master(mode):
    """
    Update all first place data.
    """
    # Define users score master table name.
    master_table_name = util.get_users_scores_master_table_name(mode)
    # Define beatmap master table name.
    first_place_table_name = util.get_first_place_table_name(mode)
    # Establish to database and get connection.
    connection = db.get_database_connection()
    # Insert user's scores data to master table.
    db.execute_update_all_first_place_master(connection, master_table_name, first_place_table_name)
    # Close database connection
    db.close_database_connection(connection)

def save_ranks_image(user_id):
    logger.info('Start to save_ranks_image.')
    # Initialize browser settings.
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=420,100')

    # Get userstats screenshot with chromedriver.
    chromedriver_filepath = '/osuRippleStats/ors/lib/chromedriver.exe'
    driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver_filepath)
    driver.get('http://localhost/ranks.php')
    driver.save_screenshot('/osuRippleStats/www/ors-images/ranks-' + str(user_id) + '.png')
    driver.quit()

    # Trimming userstats image because raw image contains scroll bars.
    image = Image.open('/osuRippleStats/www/ors-images/ranks-' + str(user_id)+ '.png')
    image_crop = image.crop((0, 0, 360, 70))
    image_crop.save('/osuRippleStats/www/ors-images/ranks-' + str(user_id) + '.png', quality=100)
    logger.info('Ended of save_ranks_image.')
