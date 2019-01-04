UPDATE
  m_beatmaps
SET
  beatmap_id = %s,
  beatmapset_id = %s,
  beatmap_md5 = '%s',
  song_name = '%s',
  ar = %s,
  od = %s,
  difficulty = %s,
  max_combo = %s,
  hit_length = %s,
  ranked = %s,
  ranked_status_frozen = %s,
  latest_update = '%s',
  mode = %s
WHERE
  beatmap_md5 = '%s'
;
