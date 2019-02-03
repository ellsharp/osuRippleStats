SELECT
  *
FROM
  t_users_badges
WHERE
  created_on = (
    SELECT
      MAX(created_on)
    FROM
      t_users_badges
    WHERE
      t_users_badges.user_id = %s
  )
;
