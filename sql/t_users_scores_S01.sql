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
) AND
  transaction.is_on_master = 0
ORDER BY
  transaction.score_id
ASC
;
