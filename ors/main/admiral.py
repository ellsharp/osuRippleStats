from ors.main.users_stats_work import UsersStatsWork
from ors.main.users_stats_transaction import UsersStatsTransaction
from ors.main.users_stats_master import UsersStatsMaster
from ors.main.users_scores_work import UsersScoresWork
from ors.main.users_scores_transaction import UsersScoresTransaction
from ors.main.users_scores_master import UsersScoresMaster
from ors.main.beatmap_master import BeatmapMaster
from ors.main.users_activity import UsersActivity
from ors.main.first_place_master import FirstPlaceMaster
from ors.script import logger
import os
import sys

if __name__ == "__main__":
    from ors.main.admiral import Admiral
    Admiral().execute()

class Admiral(object):
    global log
    log = logger.logger('admiral')

    def execute(self):
        self.__execute_shell(UsersStatsWork(), 'UsersStatsWork')
        self.__execute_shell(UsersStatsTransaction(), 'UsersStatsTransaction')
        self.__execute_shell(UsersStatsMaster(), 'UsersStatsMaster')
        self.__execute_shell(UsersScoresWork(), 'UsersScoresWork')
        self.__execute_shell(BeatmapMaster(), 'BeatmapMaster')
        self.__execute_shell(UsersScoresTransaction(), 'UsersScoresTransaction')
        self.__execute_shell(UsersScoresMaster(), 'UsersScoresMaster')
        self.__execute_shell(FirstPlaceMaster(), 'FirstPlaceMaster')
        self.__execute_shell(UsersActivity(), 'UsersActivity')

    def __execute_shell(self, constructor, process_name):
        log.info('ORSI0001', process_name)
        try:
            constructor.execute()
        except Exception as e:
            log.critical('ORSC0001', process_name, e)
        log.info('ORSI0002', process_name)
