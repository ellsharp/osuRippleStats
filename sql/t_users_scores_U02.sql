UPDATE
  t_users_scores
SET
  is_on_activity = %s
WHERE
  score_id = %s
;
