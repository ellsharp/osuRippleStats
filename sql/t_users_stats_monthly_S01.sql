SELECT
  COUNT(*) AS count
FROM
  t_users_stats_monthly
WHERE
  t_users_stats_monthly.month = '%s' AND
  t_users_stats_monthly.user_id = %s
;
