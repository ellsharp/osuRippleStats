UPDATE
  m_users_scores
SET
  user_id = %s,
  score_id = %s,
  beatmap_md5 = '%s',
  max_combo = %s,
  score = %s,
  is_full_combo = %s,
  mods = %s,
  count_300 = %s,
  count_100 = %s,
  count_50 = %s,
  count_geki = %s,
  count_katu = %s,
  count_miss = %s,
  time = '%s',
  play_mode = %s,
  accuracy = %s,
  pp = %s,
  rank = '%s',
  completed = %s
WHERE
  beatmap_md5 = '%s'
;
