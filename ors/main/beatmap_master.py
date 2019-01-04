import sys
import os
from ors.script.ripple_api import RippleApi
from ors.script import converter
from ors.script import database
from ors.script import logger

if __name__ == "__main__":
    from ors.main.beatmap_master import BeatmapMaster
    BeatmapMaster().execute()

class BeatmapMaster(object):
    global log
    log = logger.logger('BeatmapMaster')

    def execute(self):
        self.__set_beatmap_master()

    def __set_beatmap_master(self):
        result = database.execute_statement('w_beatmaps_S01')
        work_beatmaps = result[1]
        for work_beatmap in work_beatmaps:
            result = database.execute_statement('m_beatmaps_S01', work_beatmap['beatmap_md5'])
            work_beatmap['song_name'] = work_beatmap['song_name'].replace('\'', '\\\'')
            count = result[0]
            if count == 0:
                del work_beatmap['updated_on']
                result = database.execute_statement_values('m_beatmaps_I01', work_beatmap.values())
            else:
                master_beatmap = result[1][0]
                master_beatmap_latest_update = master_beatmap['latest_update']
                work_beatmap_latest_update = work_beatmap['latest_update']
                if master_beatmap_latest_update < work_beatmap_latest_update:
                    del work_beatmap['created_on']
                    del work_beatmap['updated_on']
                    work_beatmap.update(beatmap_md5_key=work_beatmap['beatmap_md5'])
                    result = database.execute_statement_values('m_beatmaps_U01', work_beatmap.values())
