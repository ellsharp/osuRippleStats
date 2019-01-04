SELECT
  *
FROM
  w_beatmaps work
WHERE NOT EXISTS(
  SELECT
    'X'
  FROM
    m_beatmaps master
  WHERE
    master.beatmap_id = work.beatmap_id
)
GROUP BY
  work.beatmap_id
;
