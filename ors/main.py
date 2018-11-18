import time
import sys
import os
from ors import util
from ors import core
from ors import logger
from ors import ripple_api

if __name__ == "__main__":
    # Read config file.
    config = util.get_config_object()

    user_id = 70666
    ripple_token = config['token']['X-Ripple-Token']

    mode = 0
    """
    users_stats = core.get_users_stats(ripple_token, user_id, mode)
    core.update_users_stats_work(users_stats, user_id, mode)
    core.update_users_stats_transaction(user_id, mode)
    core.update_users_stats_master(user_id, mode)

    print('Hitoyasumi...')
    time.sleep(1)
    """
    users_scores = core.get_users_scores_recent(ripple_token, user_id, mode)
    core.update_users_scores_work(users_scores, user_id, mode)
    core.update_users_scores_transaction(user_id, mode)
    core.update_users_scores_master(user_id, mode)
