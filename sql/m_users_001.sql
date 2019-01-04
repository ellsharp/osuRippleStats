SELECT
  COUNT(*) AS count
FROM
  ors.m_users
WHERE
  user_id = %s
;
