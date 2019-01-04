INSERT INTO
  ors.w_users_silence_info(
    user_id,
    reason,
    end,
    created_on
  )
VALUES (
  %s,
  '%s',
  '%s',
  '%s'
)
;
