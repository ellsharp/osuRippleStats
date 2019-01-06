SELECT
  *
FROM
  t_users_scores transaction
WHERE NOT EXISTS(
  SELECT
    *
  FROM
    m_users_scores master
  WHERE
    master.score_id = transaction.score_id AND
    transaction.user_id = %s
) AND NOT EXISTS (
  SELECT
    *
  FROM
    l_scores_on_master list
  WHERE
    list.score_id = transaction.score_id
)
ORDER BY
  transaction.score_id
ASC
;
