SELECT
  *
FROM
  m_users_scores
WHERE
  user_id = %s AND
  beatmap_md5 = '%s'
;
