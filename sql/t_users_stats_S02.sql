SELECT
  date_format(created_on, '%%Y-%%m') AS created_on,
  COUNT(*) AS count
FROM
  t_users_stats
WHERE
  user_id = %s
GROUP BY
  date_format(created_on, '%%Y-%%m')
ORDER BY
  date_format(created_on, '%%Y-%%m')
ASC
;
