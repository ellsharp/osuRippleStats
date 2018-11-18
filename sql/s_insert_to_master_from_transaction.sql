INSERT INTO
  %s
SELECT
  *
FROM
  %s transaction
WHERE
  transaction.score_id = %s
;
