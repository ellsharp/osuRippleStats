INSERT INTO
  t_users_scores
SELECT
  *
FROM
  w_users_scores work
WHERE NOT EXISTS(
  SELECT
    'X'
  FROM
    t_users_scores transaction
  WHERE
    transaction.score_id = work.score_id
)
;
