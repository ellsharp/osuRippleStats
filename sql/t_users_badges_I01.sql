INSERT INTO
  t_users_badges
SELECT
  *
FROM
  w_users_badges work
WHERE
  work.user_id = %s
AND NOT EXISTS(
  SELECT
    *
  FROM
    t_users_badges transaction
  WHERE
    transaction.created_on = work.created_on
);
