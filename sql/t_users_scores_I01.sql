INSERT INTO
  t_users_scores
SELECT
  *
FROM
  w_users_scores work
WHERE
  work.user_id = %s
AND NOT EXISTS(
  SELECT
    *
  FROM
    t_users_scores transaction
  WHERE
    transaction.score_id = work.score_id
);
