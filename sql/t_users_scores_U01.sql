UPDATE
  t_users_scores
SET
  is_on_master = 1
WHERE
  score_id = %s
;
