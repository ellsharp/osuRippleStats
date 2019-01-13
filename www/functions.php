<?php
  function get_mode_name_short($mode) {
    if ($mode == 0) { return 'std'; }
    else if ($mode == 1) { return 'taiko'; }
    else if ($mode == 2) { return 'ctb'; }
    else if ($mode == 3) { return 'mania'; }
  }
  function get_mode_name_full($mode) {
    if ($mode == 0) { return 'osu!'; }
    else if ($mode == 1) { return 'Taiko'; }
    else if ($mode == 2) { return 'Catch the Beat'; }
    else if ($mode == 3) { return 'osu!mania'; }
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
  function get_users_stats($user_id, $mode_num) {
    $pdo = get_pdo();
    $query = 'SELECT * FROM m_users_stats WHERE user_id = :user_id AND updated_on = (SELECT MAX(updated_on) FROM m_users_stats WHERE user_id = :user_id)';
    $statement = $pdo -> prepare($query);
    $statement -> execute([':user_id' => $user_id]);
    $users_stats = array();
    $mode_name = get_mode_name_short($mode_num);
    while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
      $users_stats += array('user_id' => $row['user_id']);
      $users_stats += array('username' => $row['username']);
      $users_stats += array('username_aka' => $row['username_aka']);
      $users_stats += array('registered_on' => $row['registered_on']);
      $users_stats += array('privileges' => $row['privileges']);
      $users_stats += array('latest_activity' => $row['latest_activity']);
      $users_stats += array('country' => $row['country']);
      $users_stats += array('ranked_score' => $row['ranked_score_'.$mode_name]);
      $users_stats += array('total_score' => $row['total_score_'.$mode_name]);
      $users_stats += array('playcount' => $row['playcount_'.$mode_name]);
      $users_stats += array('replays_watched' => $row['replays_watched_'.$mode_name]);
      $users_stats += array('total_hits' => $row['total_hits_'.$mode_name]);
      $users_stats += array('level' => $row['level_'.$mode_name]);
      $users_stats += array('accuracy' => $row['accuracy_'.$mode_name]);
      $users_stats += array('pp' => $row['pp_'.$mode_name]);
      $users_stats += array('global_leaderboard_rank' => $row['global_leaderboard_rank_'.$mode_name]);
      $users_stats += array('country_leaderboard_rank' => $row['country_leaderboard_rank_'.$mode_name]);
      $users_stats += array('play_style' => $row['play_style']);
      $users_stats += array('favourite_mode' => $row['favourite_mode']);
    }
    return $users_stats;
  }
  function get_users_max_combo($user_id, $mode_num) {
    $pdo = get_pdo();
    $query = 'SELECT MAX(max_combo) AS max_combo FROM m_users_scores WHERE user_id = :user_id AND play_mode = :mode_num';
    $statement = $pdo -> prepare($query);
    $statement -> execute([':user_id' => $user_id, 'mode_num' => $mode_num]);
    while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
      $max_combo = $row['max_combo'];
    }
    return $max_combo;
  }
  function get_users_ranks_count($user_id, $mode_num) {
    $pdo = get_pdo();
    $query = 'SELECT rank, COUNT(rank) AS count FROM m_users_scores WHERE user_id = :user_id AND play_mode = :mode_num GROUP BY rank';
    $statement = $pdo -> prepare($query);
    $statement -> execute([':user_id' => $user_id, 'mode_num' => $mode_num]);
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
    $rank_count = array('ss' => $count_ss, 's' => $count_s, 'a' => $count_a);
    return $rank_count;
  }
  function get_users_activity($user_id, $limit) {
    $pdo = get_pdo();
    $query = 'SELECT * FROM t_users_activity WHERE user_id = :user_id ORDER BY archived_on DESC';
    $statement = $pdo -> prepare($query);
    $statement -> execute([':user_id' => $user_id]);
    $counter = 0;
    $users_activity = array();
    while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
      $users_activity_temp = array();
      $users_activity_temp += array('archived_on' => $row['archived_on']);
      $users_activity_temp += array('song_name' => $row['song_name']);
      $users_activity_temp += array('beatmap_id' => $row['beatmap_id']);
      $users_activity_temp += array('type' => $row['type']);
      $users_activity_temp += array('ranking' => $row['ranking']);
      $users_activity_temp += array('rank' => $row['rank']);
      $users_activity_temp += array('mode' => $row['mode']);
      $users_activity += array($counter => $users_activity_temp);
      $counter += 1;
      if ($counter > $limit) { break; }
    }
    return $users_activity;
  }
  function get_users_pp_rank_history($user_id, $mode_num) {
    $pdo = get_pdo();
    $mode_name = get_mode_name_short($mode_num);
    $global_leaderboard_rank = 'global_leaderboard_rank_'.$mode_name;
    $query = 'SELECT date_format(created_on, \'%Y-%m-%d\') AS date, MAX('.$global_leaderboard_rank.') AS pp_rank FROM t_users_stats WHERE user_id = :user_id GROUP BY date_format(created_on, \'%Y-%m-%d\') ORDER BY pp_rank DESC;';
    $statement = $pdo -> prepare($query);
    $statement -> execute([':user_id' => $user_id]);
    $date = [];
    $pp_rank = [];
    $counter = 0;
    while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
      $date[] = $row['date'];
      $pp_rank[] = $row['pp_rank'];
      $counter += 1;
      if ($counter > 90) { break; }
    }
    $pp_rank_history = [];
    $pp_rank_history[] = $date;
    $pp_rank_history[] = $pp_rank;
    return $pp_rank_history;
  }
  function get_datetime_diff($datetime) {
    $now = new Datetime();
    $datetime = new Datetime($datetime);
    $month = date_diff($datetime, $now) -> format('%m');
    $day = date_diff($datetime, $now) -> format('%d');
    $hour = date_diff($datetime, $now) -> format('%h');
    $minute = date_diff($datetime, $now) -> format('%i');
    if ($month > 1) {
      return $month.' months ago';
    } else if ($day > 1) {
      return $day.' days ago';
    } else if ($day > 0) {
      return 'about '.(24 + $hour).' hours ago';
    } else if ($hour > 0) {
      return 'about '.$hour.' hours ago';
    } else if ($minute > 0) {
      return $minute.' minutes ago';
    } else {
      return 'less than minute ago';
    }
  }
  function print_users_activity($user_id, $username) {
    $users_activity = get_users_activity($user_id, 30);
    $counter = 0;
    print('<div class="ui two column grid attached segment">');
    foreach ($users_activity as $activity) {
      $type = $activity['type'];
      $ranking = $activity['ranking'];
      $archived_on = $activity['archived_on'];
      $rank = $activity['rank'];
      $beatmap_id = $activity['beatmap_id'];
      $song_name = $activity['song_name'];
      $mode_name = get_mode_name_full($activity['mode']);
      if ($type != 2 and $ranking < 51) {
        print('<div class="three wide column attached segment">');
        print('<p>'.get_datetime_diff($archived_on).'</p>');
        print('</div>');
        print('<div class="thirteen wide column attached segment">');
        print('<p>');
        print('<img src="/images/'.$rank.'_small.png" style="padding-right: 8px"/>');
        print($username.' archived rank ');
        if ($ranking < 4) {
          print('<b>#'.$ranking.'</b> on <a href="https://ripple.moe/b/'.$beatmap_id.'">'.$song_name.'</a> ('.$mode_name.')');
        } else {
          print('#'.$ranking.' on <a href="https://ripple.moe/b/'.$beatmap_id.'">'.$song_name.'</a> ('.$mode_name.')');
        }
        print('</p>');
        print('</div>');
      } else if ($type == 2) {
        print('<div class="three wide column attached segment">');
        print('<p>'.get_datetime_diff($archived_on).'</p>');
        print('</div>');
        print('<div class="thirteen wide column attached segment">');
        print('<p>');
        print($username.' has lost first place on on <a href="https://ripple.moe/b/'.$beatmap_id.'">'.$song_name.'</a> ('.$mode_name.')');
        print('</p>');
        print('</div>');
      }
      $counter += 1;
    }
    print('</div>');
  }
  function print_first_place_ranks($user_id, $mode_num) {
    $pdo = get_pdo();
    $query = 'SELECT m_first_place.score_id AS score_id, m_first_place.mods AS mods, m_first_place.rank AS rank, m_first_place.time AS time, m_first_place.accuracy AS accuracy, m_first_place.pp AS pp, m_beatmaps.song_name, m_beatmaps.beatmap_id as beatmap_id FROM m_first_place INNER JOIN  m_beatmaps ON m_first_place.beatmap_md5 = m_beatmaps.beatmap_md5 WHERE m_first_place.user_id = :user_id AND m_first_place.play_mode = :mode_num ORDER BY time DESC;';
    $statement = $pdo -> prepare($query);
    $statement -> execute([':user_id' => $user_id, 'mode_num' => $mode_num]);
    print('<div class="ui attached segments">');
    while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
      $rank = $row['rank'];
      $song_name = $row['song_name'];
      $mods = $row['mods'];
      $accuracy = $row['accuracy'];
      $time = $row['time'];
      $pp = $row['pp'];
      $score_id = $row['score_id'];
      $beatmap_id = $row['beatmap_id'];
      print('<div class="ui horizontal two column grid attached segment" style="margin: 0">');
      print('<div class="thirteen wide column left aligned">');
      print('<p>');
      print('<img src="/images/'.$rank.'_small.png" style="padding-right: 8px">');
      print('<a href="https://ripple.moe/b/'.$beatmap_id.'">'.$song_name.' ('.sprintf('%0.2f', $accuracy).'%)</a>');
      print('</p>');
      print('<p>'.get_datetime_diff($time).'</p>');
      print('</div>');
      print('<div class="three wide column right aligned">');
      print('<p>'.sprintf('%d', $pp).'pp</p>');
      print('<p><a href="https://ripple.moe/web/replays/'.$score_id.'"><i class="star link icon"></i></a></p>');
      print('</div>');
      print('</div>');
    }
    print('</div>');
  }
  function print_pp_chart_label($date) {
    for ($i = count($date); 0 < $i; $i--) {
      print('"'.$i.'", ');
    }
  }
  function print_pp_chart_data($pp_rank) {
    for ($i = 0; $i < count($pp_rank); $i++) {
      print($pp_rank[$i].',');
    }
  }
?>
