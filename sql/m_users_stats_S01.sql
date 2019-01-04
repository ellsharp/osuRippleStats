SELECT
  COUNT(*) count
FROM
  m_users_stats
WHERE
  user_id = %s
;
