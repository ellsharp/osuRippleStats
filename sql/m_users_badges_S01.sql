SELECT
  COUNT(*) count
FROM
  m_users_badges
WHERE
  user_id = %s
;
