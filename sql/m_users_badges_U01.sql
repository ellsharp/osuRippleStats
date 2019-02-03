UPDATE
  m_users_badges
SET
  user_id = %s,
  badge_id = %s,
  name = '%s',
  icon = '%s'
WHERE
  user_id = %s AND
  badge_id = %s
;
