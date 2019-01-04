SELECT
  beatmap_id,
  song_name
FROM
  m_beatmaps
WHERE
  beatmap_md5 = '%s'
;
