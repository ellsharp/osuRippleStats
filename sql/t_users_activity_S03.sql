SELECT
  MAX(score) as score
FROM
  t_users_activity
WHERE
  beatmap_md5 = '%s'
;
