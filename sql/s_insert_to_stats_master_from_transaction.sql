INSERT INTO
  %s
SELECT
  *
FROM
  %s transaction
WHERE
  transaction.user_id = %s
;
