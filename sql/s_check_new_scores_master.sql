SELECT
  new_scores.score_id
FROM (
  SELECT
    transaction.user_id,
    transaction.score_id,
    transaction.beatmap_md5,
    transaction.score,
    transaction.max_combo,
    transaction.is_full_combo,
    transaction.mods,
    transaction.count_300,
    transaction.count_100,
    transaction.count_50,
    transaction.count_geki,
    transaction.count_katu,
    transaction.count_miss,
    transaction.time,
    transaction.play_mode,
    transaction.accuracy,
    transaction.pp,
    transaction.rank,
    transaction.completed,
    transaction.created_on,
    transaction.created_by,
    transaction.updated_on,
    transaction.updated_by
  FROM
    %s AS transaction
    INNER JOIN(
      SELECT
        beatmap_md5,
        MAX(score) AS score
      FROM
        %s
      GROUP BY
        beatmap_md5
    ) AS transaction_classified
    ON
      transaction.beatmap_md5 = transaction_classified.beatmap_md5
      AND
      transaction.score = transaction_classified.score
) AS new_scores
LEFT OUTER JOIN
  %s master
ON
  new_scores.score_id = master.score_id
WHERE
  master.score_id IS NULL
;
