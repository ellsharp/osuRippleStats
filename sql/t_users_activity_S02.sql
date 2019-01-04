SELECT
  *
FROM
  t_users_scores scores
WHERE NOT EXISTS(
  SELECT
    'X'
  FROM
    t_users_activity activity
  WHERE
    scores.score_id = activity.score_id AND
    activity.user_id = %s
) AND
  scores.is_on_activity = 0
ORDER BY
  scores.time
ASC
;
