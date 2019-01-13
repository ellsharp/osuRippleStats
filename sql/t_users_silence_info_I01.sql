INSERT INTO
  t_users_silence_info
SELECT
  *
FROM
  w_users_silence_info work
WHERE
  work.user_id = %s
AND NOT EXISTS(
  SELECT
    *
  FROM
    t_users_silence_info transaction
  WHERE
    transaction.created_on = work.created_on
);
