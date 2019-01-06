<?php
  $pdo = get_pdo();
  $query = 'SELECT * FROM m_users_stats WHERE user_id = 70666 AND updated_on = (SELECT MAX(updated_on) FROM m_users_stats WHERE user_id = 70666)';
  $statement = $pdo -> prepare($query);
  $statement -> execute();
  while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
    $username = $row['username'];
    $pp_std = $row['pp_std'];
    $global_leaderboard_rank_std = $row['global_leaderboard_rank_std'];
    $country_leaderboard_rank_std = $row['country_leaderboard_rank_std'];
    $ranked_score = $row['ranked_score_std'];
    $accuracy = $row['accuracy_std'];
    $playcount = $row['playcount_std'];
    $total_score = $row['total_score_std'];
    $level = $row['level_std'];
    $total_hits = $row['total_hits_std'];
    $replays_watched = $row['replays_watched_std'];
  }
  $query = 'SELECT MAX(max_combo) AS max_combo FROM m_users_scores WHERE user_id = 70666 AND play_mode = 0';
  $statement = $pdo -> prepare($query);
  $statement -> execute();
  while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
    $max_combo = $row['max_combo'];
  }

  $query = 'SELECT rank, COUNT(rank) AS count FROM m_users_scores GROUP BY rank';
  $statement = $pdo -> prepare($query);
  $statement -> execute();
  $count_ss = 0;
  $count_s  = 0;
  $count_a  = 0;
  while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
    if ($row['rank'] == 'SSH' or $row['rank'] == 'SS') {
      $count_ss = $count_ss + $row['count'];
    } else if ($row['rank'] == 'SH' or $row['rank'] == 'S') {
      $count_s = $count_s + $row['count'];
    } else if ($row['rank'] == 'A') {
      $count_a = $count_a + $row['count'];
    }
  }
  function get_pdo(){
    $database_config = parse_ini_file('../conf/database.conf');
    $db_dbname = $database_config['dbname'];
    $db_host = $database_config['host'];
    $db_port = $database_config['port'];
    $db_charset = $database_config['charset'];
    $db_user = $database_config['user'];
    $db_password = $database_config['password'];

    # Connect to database.
    $dsn = 'mysql:dbname='.$db_dbname.'; host='.$db_host.'; port='.$db_port.'; charset='.$db_charset;
    $pdo = new PDO($dsn, $db_user, $db_password);
    return $pdo;
  }
  function get_gamemode($mode) {
    if ($mode == 0) {
      return 'osu!';
    } else if ($mode == 1) {
      return 'Taiko';
    } else if ($mode == 2) {
      return 'Catch the Beat';
    } else if ($mode == 3) {
      return 'osu!mania';
    }
  }
  function get_users_pp_rank_history($mode) {
    $query = 'select date_format(created_on, \'%Y-%m-%d\') as date, MAX(global_leaderboard_rank_std) as pp_rank from t_users_stats group by date_format(created_on, \'%Y-%m-%d\') ORDER BY pp_rank DESC;';
    $pdo = get_pdo();
    $statement = $pdo -> prepare($query);
    $statement -> execute();

    $date = [];
    $pp_rank = [];
    $counter = 0;
    while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
      $date[] = $row['date'];
      $pp_rank[] = $row['pp_rank'];
      $counter = $counter + 1;
      if ($counter > 90) {
        break;
      }
    }
    $return = [];
    $return[] = $date;
    $return[] = $pp_rank;
    return $return;
  }
  $result = get_users_pp_rank_history(0);
  $date = $result[0];
  $pp_rank =$result[1];
  function print_label($date) {
    for ($i = 0; $i < count($date); $i++) {
      if ($i == 29) {
        print('"ALOHA", ');
      } else {
        print('"", ');
        //print($date[$i].',');
      }
    }
  }
  function print_data($pp_rank) {
    for ($i = 0; $i < count($pp_rank); $i++) {
      print($pp_rank[$i].',');
    }
  }
  function print_activity() {
    $query = 'SELECT * FROM t_users_activity WHERE user_id = 70666 ORDER BY archived_on DESC';
    $pdo = get_pdo();
    $statement = $pdo -> prepare($query);
    $statement -> execute();

    $counter = 0;
    while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
      $archived_on = $row['archived_on'];
      $song_name = $row['song_name'];
      $beatmap_id = $row['beatmap_id'];
      $type = $row['type'];
      $ranking = $row['ranking'];
      $rank = $row['rank'];
      $mode = $row['mode'];

      if ($type != 2) {
        if ($ranking < 51) {
          print('<tr>');
          print('<td class="activity-time">'.get_datetime_diff($archived_on).'</td>');
          print('<td class="activity-detail">');
          print('<img src="/images/'.$rank.'_small.png" />');
          print('ellsharp archived rank #'.$ranking.' on <a href="https://ripple.moe/b/'.$beatmap_id.'">'.$song_name.'</a> ('.get_gamemode($mode).')');
          print('</td>');
          print('<tr>');
        }
      }
      $counter++;
      if ($counter > 16) {
        break;
      }
    }
  }
  function get_datetime_diff($datetime) {
    $now = new Datetime();
    $datetime = new Datetime($datetime);
    $day = date_diff($datetime, $now) -> format('%d');
    $hour = date_diff($datetime, $now) -> format('%h');
    $minute = date_diff($datetime, $now) -> format('%i');
    if ($day > 1) {
      return $day.' days ago';
    } else if ($day > 0) {
      return 'about '.(24 + $hour).' hours ago';
    } else if ($hour > 0) {
      return 'about '.$hour.' hours ago';
    } else {
      return $minute.' minutes ago';
    }

    return date_diff($datetime, $now);
  }
?>
