import sys
import os
from ors.script.database import Database
from ors.script import converter
from ors.script import logger

if __name__ == "__main__":
    from ors.main.beatmap_master import BeatmapMaster
    BeatmapMaster().execute()

class BeatmapMaster(object):
    global log
    global database
    global connection
    log = logger.logger('beatmap_master')
    database = Database()
    connection = database.get_connection()

    def execute(self):
        try:
            log.info('ORSI0001', 'BeatmapMaster')
            self.__set_beatmap_master()
            connection.commit()
            connection.close()
            log.info('ORSI0002', 'BeatmapMaster')
        except Exception as e:
            log.critical('ORSC0001', 'BeatmapMaster', e)
            raise Exception(e)

    def __set_beatmap_master(self):
        # Insert new beatmaps from work to master.
        result = database.execute_statement(connection, 'm_beatmaps_S03')
        count = result[0]
        new_beatmaps = result[1]
        log.info('ORSI0008', count)
        for new_beatmap in new_beatmaps:
            del new_beatmap['updated_on']
            song_name = new_beatmap['song_name']
            new_beatmap['song_name'] = new_beatmap['song_name'].replace('\'', '\\\'')
            result = database.execute_statement_values(connection, 'm_beatmaps_I01', new_beatmap.values())
            log.debug('ORSD0008', song_name, new_beatmap['beatmap_id'], new_beatmap['beatmap_md5'])
        # Insert updated beatmaps from work to master
        result = database.execute_statement(connection, 'm_beatmaps_S04')
        count = result[0]
        updated_beatmaps = result[1]
        log.info('ORSI0009', count)
        for updated_beatmap in updated_beatmaps:
            del updated_beatmap['created_on']
            del updated_beatmap['updated_on']
            song_name = updated_beatmap['song_name']
            updated_beatmap.update(beatmap_md5_key=updated_beatmap['beatmap_md5'])
            song_name = updated_beatmap['song_name']
            updated_beatmap['song_name'] = updated_beatmap['song_name'].replace('\'', '\\\'')
            result = database.execute_statement_values(connection, 'm_beatmaps_U01', updated_beatmap.values())
            log.debug('ORSD0009', song_name, updated_beatmap['beatmap_id'], updated_beatmap['beatmap_md5'], updated_beatmap['latest_update'])
