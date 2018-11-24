import time
from ors import core
from ors import util
from ors import db
from ors import peppy_api

if __name__ == "__main__":
    # Read config file.
    config = util.get_config_object()

    user_id = 70666
    mode = 0
    ripple_token = config['token']['X-Ripple-Token']
    #users_scores = core.get_users_scores_recent(ripple_token, user_id, mode)
    #print(users_scores)
    beatmap_md5 = '0b3fc409ebbcd28d14b2baa117161464'
    #beatmap_data = peppy_api.get_beatmaps(beatmap_md5, mode, 0, 1)
    #print(beatmap_data)
    beatmap_id = util.get_beatmap_id(beatmap_md5, mode)
    print(beatmap_id)
    #core.update_beatmap_master(beatmap_data, mode)
"""
    connection = db.get_database_connection()
    try:
        cursor = connection.cursor()
        # Execute Statement
        cursor.execute('SELECT beatmap_md5 FROM m_users_scores_std WHERE user_id = %s' % user_id)
        for row in cursor:
            beatmap_md5 = row['beatmap_md5']
            if (core.is_first_place_ranks(ripple_token, user_id, beatmap_md5, mode)):
                print('%s is champion.' % beatmap_md5)
                time.sleep(1)
        cursor.close()
    except Exception as e:
        # When failed to commit statement, rollback table and system abnormal end.
        sys.exit(1)
"""
