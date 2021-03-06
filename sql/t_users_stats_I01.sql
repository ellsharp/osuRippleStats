INSERT INTO
  t_users_stats
SELECT
  *
FROM
  w_users_stats work
WHERE
  work.user_id = %s
AND NOT EXISTS(
  SELECT
    *
  FROM
    t_users_stats transaction
  WHERE
    transaction.created_on = work.created_on
);
