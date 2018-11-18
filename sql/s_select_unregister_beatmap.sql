SELECT
  m_scores.beatmap_md5
FROM
  %s m_scores
LEFT OUTER JOIN
  %s m_beatmaps
ON
  m_scores.beatmap_md5 = m_beatmaps.file_md5
WHERE
  m_beatmaps.file_md5 IS NULL
;
