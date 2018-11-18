SELECT
  work.score_id
FROM
  %s work
LEFT OUTER JOIN
  %s transaction
ON
  work.score_id = transaction.score_id
WHERE
  transaction.score_id IS NULL
;
