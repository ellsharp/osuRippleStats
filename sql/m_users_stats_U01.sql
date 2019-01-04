UPDATE
  m_users_stats
SET
  user_id = %s,
  username = '%s',
  username_aka = '%s',
  registered_on = '%s',
  privileges = %s,
  latest_activity = '%s',
  country = '%s',
  ranked_score_std = %s,
  total_score_std = %s,
  playcount_std = %s,
  replays_watched_std = %s,
  total_hits_std = %s,
  level_std = %s,
  accuracy_std = %s,
  pp_std = %s,
  global_leaderboard_rank_std = %s,
  country_leaderboard_rank_std = %s,
  ranked_score_taiko = %s,
  total_score_taiko = %s,
  playcount_taiko = %s,
  replays_watched_taiko = %s,
  total_hits_taiko = %s,
  level_taiko = %s,
  accuracy_taiko = %s,
  pp_taiko = %s,
  global_leaderboard_rank_taiko = %s,
  country_leaderboard_rank_taiko = %s,
  ranked_score_ctb = %s,
  total_score_ctb = %s,
  playcount_ctb = %s,
  replays_watched_ctb = %s,
  total_hits_ctb = %s,
  level_ctb = %s,
  accuracy_ctb = %s,
  pp_ctb = %s,
  global_leaderboard_rank_ctb = %s,
  country_leaderboard_rank_ctb = %s,
  ranked_score_mania = %s,
  total_score_mania = %s,
  playcount_mania = %s,
  replays_watched_mania = %s,
  total_hits_mania = %s,
  level_mania = %s,
  accuracy_mania = %s,
  pp_mania = %s,
  global_leaderboard_rank_mania = %s,
  country_leaderboard_rank_mania = %s,
  play_style = %s,
  favourite_mode = %s
WHERE
  user_id = %s
;