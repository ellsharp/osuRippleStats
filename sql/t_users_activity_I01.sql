INSERT INTO
  t_users_activity(
    user_id,
    score_id,
    beatmap_id,
    beatmap_md5,
    song_name,
    ranking,
    type,
    mode,
    rank,
    archived_on,
    created_on
  )
VALUES (
  %s,
  %s,
  %s,
  '%s',
  '%s',
  %s,
  %s,
  %s,
  '%s',
  '%s',
  '%s'
)
;