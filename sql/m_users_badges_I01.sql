INSERT INTO
  m_users_badges(
    user_id,
    badge_id,
    name,
    icon,
    created_on
  )
VALUES (
  %s,
  %s,
  '%s',
  '%s',
  '%s'
)
;
