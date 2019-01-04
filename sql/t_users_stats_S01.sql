SELECT
  *
FROM
  t_users_stats
WHERE
  created_on = (
    SELECT
      MAX(created_on)
    FROM
      t_users_stats
    WHERE
      t_users_stats.user_id = %s
  )
;
