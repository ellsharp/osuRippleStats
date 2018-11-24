import time
import sys
import os
from ors import util
from ors import core
from ors import logger
from ors import ripple_api

if __name__ == "__main__":

    user_id = 70666
    mode = 0

    core.update_users_stats_work(user_id, mode)
    core.update_users_stats_transaction(user_id, mode)
    core.update_users_stats_master(user_id, mode)

    print('Hitoyasumi...')
    time.sleep(1)

    core.update_users_scores_work(user_id, mode)
    core.update_users_scores_transaction(user_id, mode)
    core.update_users_scores_master(user_id, mode)
