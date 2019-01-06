SELECT
  *
FROM
  t_users_scores scores
WHERE NOT EXISTS(
  SELECT
    *
  FROM
    t_users_activity activity
  WHERE
    scores.score_id = activity.score_id AND
    activity.user_id = %s
) AND NOT EXISTS (
  SELECT
    *
  FROM
    l_scores_on_activity list
  WHERE
    list.score_id = scores.score_id
)
ORDER BY
  scores.time
ASC
;
