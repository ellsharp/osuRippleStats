SELECT
  score_id,
  beatmap_md5
FROM
  t_users_activity
WHERE NOT EXISTS(
  SELECT
    'X'
  FROM
    m_first_place
  WHERE
    t_users_activity.score_id = m_first_place.score_id
) AND
  t_users_activity.type = 1 AND
  t_users_activity.user_id = %s
ORDER BY
  t_users_activity.score_id
ASC;
