SELECT
  *
FROM
  w_beatmaps work
WHERE
  work.beatmap_id = (
    SELECT
      beatmap_id
    FROM
      m_beatmaps master
    WHERE
      master.beatmap_id = work.beatmap_id AND
      master.latest_update < work.latest_update
    GROUP BY
      master.beatmap_id
  );
