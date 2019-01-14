SELECT
  *
FROM
  t_users_stats
WHERE
  t_users_stats.created_on = (
    SELECT
      MAX(created_on)
    FROM
      t_users_stats
    WHERE
      created_on like '%s%%' AND
      user_id = %s
  )
AND
  user_id = %s
;
