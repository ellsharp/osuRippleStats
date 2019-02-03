INSERT INTO
  s_api_request_count_hourly
SELECT
  DATE_FORMAT(datetime, '%%Y-%%m-%%d %%H:00:00') AS datetime,
  SUM(count) AS count
FROM
  s_api_request_count_tick
GROUP BY
 DATE_FORMAT(datetime, '%%Y-%%m-%%d %%H:00:00');
