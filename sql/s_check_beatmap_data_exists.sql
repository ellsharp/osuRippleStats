SELECT
  COUNT(*) AS count
FROM
  %s
WHERE
  file_md5 = '%s'
;
