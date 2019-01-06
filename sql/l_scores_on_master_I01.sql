INSERT INTO
  l_scores_on_master(
    user_id,
    score_id,
    type,
    created_on
  ) VALUES (
    %s,
    %s,
    %s,
    '%s'
  );
