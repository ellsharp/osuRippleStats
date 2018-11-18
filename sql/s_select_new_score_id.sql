SELECT
  COUNT(beatmap_md5) AS count
FROM
  %s master
WHERE
  master.beatmap_md5 = (
    SELECT
      beatmap_md5
    FROM
      %s
    WHERE
      score_id = %s
  )
;
