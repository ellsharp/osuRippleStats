UPDATE
  %s AS master,
  (
     SELECT
       *
     FROM
       %s
     WHERE
       created_on = (
         SELECT
           MAX(created_on) AS created_on
         FROM
           %s
       )
  ) AS transaction
SET
  master.user_id = transaction.user_id,
  master.username = transaction.username,
  master.username_aka = transaction.username_aka,
  master.registered_on = transaction.registered_on,
  master.privileges = transaction.privileges,
  master.latest_activity = transaction.latest_activity,
  master.country = transaction.country,
  master.ranked_score = transaction.ranked_score,
  master.total_score = transaction.total_score,
  master.playcount = transaction.playcount,
  master.replays_watched = transaction.replays_watched,
  master.total_hits = transaction.total_hits,
  master.level = transaction.level,
  master.accuracy = transaction.accuracy,
  master.pp = transaction.pp,
  master.global_leaderboard_rank = transaction.global_leaderboard_rank,
  master.country_leaderboard_rank = transaction.country_leaderboard_rank,
  master.play_style = transaction.play_style,
  master.favourite_mode = transaction.favourite_mode,
  master.created_by = transaction.created_by,
  master.updated_by = transaction.updated_by
WHERE
  master.user_id = %s
