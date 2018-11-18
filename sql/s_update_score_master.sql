UPDATE
  %s AS master,
  (
    SELECT
      *
    FROM
      %s
    WHERE
      score_id = %s
  ) AS transaction
SET
  master.user_id = transaction.user_id,
  master.score_id = transaction.score_id,
  master.beatmap_md5 = transaction.beatmap_md5,
  master.score = transaction.score,
  master.max_combo = transaction.max_combo,
  master.is_full_combo = transaction.is_full_combo,
  master.mods = transaction.mods,
  master.count_300 = transaction.count_300,
  master.count_100 = transaction.count_100,
  master.count_50 = transaction.count_50,
  master.count_geki = transaction.count_geki,
  master.count_katu = transaction.count_katu,
  master.count_miss = transaction.count_miss,
  master.time = transaction.time,
  master.play_mode = transaction.play_mode,
  master.accuracy = transaction.accuracy,
  master.pp = transaction.pp,
  master.rank = transaction.rank,
  master.completed = transaction.completed,
  master.created_on = transaction.created_on,
  master.created_by = transaction.created_by,
  master.updated_on = transaction.updated_on,
  master.updated_by = transaction.updated_by
WHERE
  master.beatmap_md5 = (
    SELECT
      beatmap_md5
    FROM
      %s
    WHERE
      score_id = %s
  )
;
