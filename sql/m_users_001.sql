SELECT
  COUNT(*) AS count
FROM
  m_users
WHERE
  user_id = %s
;
