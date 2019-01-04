INSERT INTO
  t_users_stats
SELECT
  *
FROM
  w_users_stats work
WHERE NOT EXISTS(
  SELECT
    'X'
  FROM
    t_users_stats transaction
  WHERE
    transaction.created_on = work.created_on
)
;
