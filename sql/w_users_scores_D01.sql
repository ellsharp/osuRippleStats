DELETE FROM
  w_users_scores
WHERE
  user_id = %s AND
  play_mode = %s
;
