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
    $users_best_scores = array();
    while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
      $max_combo = $row['max_combo'];
    }
    return $max_combo;
  }
  function print_best_performance_scores($user_id, $mode_num) {
    $pdo = get_pdo();
    $query = 'SELECT m_users_scores.score_id AS score_id, m_users_scores.mods AS mods, m_users_scores.rank AS rank, m_users_scores.time AS time, m_users_scores.accuracy AS accuracy, m_users_scores.pp AS pp, m_beatmaps.song_name, m_beatmaps.beatmap_id as beatmap_id FROM m_users_scores INNER JOIN  m_beatmaps ON m_users_scores.beatmap_md5 = m_beatmaps.beatmap_md5 WHERE m_users_scores.user_id = :user_id AND m_users_scores.play_mode = :mode_num ORDER BY pp DESC LIMIT 100;';
    $statement = $pdo -> prepare($query);
    $statement -> execute([':user_id' => $user_id, 'mode_num' => $mode_num]);
    $weight_percent = [100, 95, 90, 86, 81, 77, 74, 70, 66, 63,
                        60, 57, 54, 51, 49, 46, 44, 42, 38, 36,
                        34, 32, 31, 29, 28, 26, 25, 24, 23, 21,
                        20, 19, 28, 17, 17, 16, 15, 14, 14, 13,
                        12, 12, 11, 10, 10,  9,  9,  9,  8,  8,
                         7,  7,  7,  6,  6,  6,  5,  5,  5,  5,
                         4,  4,  4,  4,  4,  3,  3,  3,  3,  3,
                         3,  2,  2,  2,  2,  2,  2,  2,  2,  2,
                         2,  1,  1,  1,  1,  1,  1,  1,  1,  1,
                         1,  1,  1,  1,  1,  1,  1,  1,  1,  1];
    $counter = 0;
    while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
      $score_id = $row['score_id'];
      $mods = $row['mods'];
      $rank = $row['rank'];
      $time = $row['time'];
      $accuracy = $row['accuracy'];
      $song_name = $row['song_name'];
      $beatmap_id = $row['beatmap_id'];
      $pp = $row['pp'];
      print('<div class="ui horizontal two column grid attached segment bp" style="margin: 0">');
      print('<div class="eleven wide column left aligned">');
      print('<p style="margin-bottom: 0.5rem">');
      print('<img src="/images/'.$rank.'_small.png" style="padding-right: 8px">');
      if ($mods == 0) {
        print('<a href="https://ripple.moe/b/'.$beatmap_id.'">'.$song_name.'</a> ('.sprintf('%0.2f', $accuracy).'%)');
      } else {
        print('<a href="https://ripple.moe/b/'.$beatmap_id.'">'.$song_name.'</a> <b>+'.get_mods($mods).'</b> ('.sprintf('%0.2f', $accuracy).'%)');
      }
      print('</p>');
      print('<p>'.get_datetime_diff($time).'</p>');
      print('</div>');
      print('<div class="five wide column right aligned">');
      print('<p style="margin-bottom: 0.5rem">'.sprintf('%d', $pp).'pp</p>');
      print('<p>weighted '.$weight_percent[$counter].'% ('.sprintf('%d', $pp * ($weight_percent[$counter] / 100)).'pp) <a href="https://ripple.moe/web/replays/'.$score_id.'"><i class="star link icon"></i></a></p>');
      print('</div>');
      print('</div>');
      $counter = $counter + 1;
    }
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
  function get_users_activity($user_id) {
    $pdo = get_pdo();
    $query = 'SELECT * FROM t_users_activity WHERE user_id = :user_id ORDER BY archived_on DESC LIMIT 30';
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
  function get_users_playcount_history($user_id, $mode_num) {
    $pdo = get_pdo();
    $mode_name = get_mode_name_short($mode_num);
    $playcount = 'playcount_'.$mode_name;
    $query = 'SELECT month, '.$playcount.' AS playcount FROM t_users_stats_monthly WHERE user_id = :user_id';
    $statement = $pdo -> prepare($query);
    $statement -> execute([':user_id' => $user_id]);
    $month = [];
    $playcount = [];
    while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
      $month[] = $row['month'];
      $playcount[] = $row['playcount'];
    }
    $playcount_history = [];
    $playcount_history[] = $month;
    $playcount_history[] = $playcount;
    return $playcount_history;
  }
  function get_users_replays_history($user_id, $mode_num) {
    $pdo = get_pdo();
    $mode_name = get_mode_name_short($mode_num);
    $replays = 'replays_watched_'.$mode_name;
    $query = 'SELECT month, '.$replays.' AS replays FROM t_users_stats_monthly WHERE user_id = :user_id';
    $statement = $pdo -> prepare($query);
    $statement -> execute([':user_id' => $user_id]);
    $month = [];
    $replays = [];
    while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
      $month[] = $row['month'];
      $replays[] = $row['replays'];
    }
    $replays_history = [];
    $replays_history[] = $month;
    $replays_history[] = $replays;
    return $replays_history;
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
      return 'less than minutes ago';
    }
  }
  function print_users_activity($user_id, $username) {
    $users_activity = get_users_activity($user_id);
    $counter = 0;
    foreach ($users_activity as $activity) {
      $type = $activity['type'];
      $ranking = $activity['ranking'];
      $archived_on = $activity['archived_on'];
      $rank = $activity['rank'];
      $beatmap_id = $activity['beatmap_id'];
      $song_name = $activity['song_name'];
      $mode_name = get_mode_name_full($activity['mode']);
      if ($type != 2 and $ranking < 51) {
        print('<div class="ui three wide column left aligned" style="padding-top: 0.5rem; padding-bottom: 0.5rem">');
        print('<p>'.get_datetime_diff($archived_on).'</p>');
        print('</div>');
        print('<div class="ui thirteen wide column left aligned" style="padding-top : 0.5rem; padding-bottom: 0.5rem">');
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
        $counter += 1;
      } else if ($type == 2) {
        print('<div class="three wide column attached segment" style="padding-top: 0.5rem; padding-bottom: 0.5rem">');
        print('<p>'.get_datetime_diff($archived_on).'</p>');
        print('</div>');
        print('<div class="thirteen wide column attached segment" style="padding-top: 0.5rem; padding-bottom: 0.5rem">');
        print('<p>');
        print($username.' has lost first place on on <a href="https://ripple.moe/b/'.$beatmap_id.'">'.$song_name.'</a> ('.$mode_name.')');
        print('</p>');
        print('</div>');
        $counter += 1;
      }
      if ($counter > 15) { break; }
    }
  }
  function print_first_place_ranks($user_id, $mode_num) {
    $pdo = get_pdo();
    $query = 'SELECT m_first_place.score_id AS score_id, m_first_place.mods AS mods, m_first_place.rank AS rank, m_first_place.time AS time, m_first_place.accuracy AS accuracy, m_first_place.pp AS pp, m_beatmaps.song_name, m_beatmaps.beatmap_id as beatmap_id FROM m_first_place INNER JOIN  m_beatmaps ON m_first_place.beatmap_md5 = m_beatmaps.beatmap_md5 WHERE m_first_place.user_id = :user_id AND m_first_place.play_mode = :mode_num ORDER BY time DESC;';
    $statement = $pdo -> prepare($query);
    $statement -> execute([':user_id' => $user_id, 'mode_num' => $mode_num]);
    while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
      $rank = $row['rank'];
      $song_name = $row['song_name'];
      $mods = $row['mods'];
      $accuracy = $row['accuracy'];
      $time = $row['time'];
      $pp = $row['pp'];
      $score_id = $row['score_id'];
      $beatmap_id = $row['beatmap_id'];
      print('<div class="ui horizontal two column grid attached segment fp" style="margin: 0">');
      print('<div class="thirteen wide column left aligned">');
      print('<p style="margin-bottom: 0.5rem">');
      print('<img src="/images/'.$rank.'_small.png" style="padding-right: 8px">');
      if ($mods == 0) {
        print('<a href="https://ripple.moe/b/'.$beatmap_id.'">'.$song_name.'</a> ('.sprintf('%0.2f', $accuracy).'%)');
      } else {
        print('<a href="https://ripple.moe/b/'.$beatmap_id.'">'.$song_name.'</a> <b>+'.get_mods($mods).'</b> ('.sprintf('%0.2f', $accuracy).'%)');
      }
      print('</p>');
      print('<p>'.get_datetime_diff($time).'</p>');
      print('</div>');
      print('<div class="three wide column right aligned">');
      print('<p style="margin-bottom: 0.5rem">'.sprintf('%d', $pp).'pp</p>');
      print('<p><a href="https://ripple.moe/web/replays/'.$score_id.'"><i class="star link icon"></i></a></p>');
      print('</div>');
      print('</div>');
    }
  }
  function print_users_recent_plays($user_id, $mode_num) {
    $pdo = get_pdo();
    $query = 'SELECT t_users_scores.mods AS mods, t_users_scores.rank AS rank, t_users_scores.time AS time, t_users_scores.score AS score, m_beatmaps.song_name, m_beatmaps.beatmap_id as beatmap_id FROM t_users_scores INNER JOIN  m_beatmaps ON t_users_scores.beatmap_md5 = m_beatmaps.beatmap_md5 WHERE t_users_scores.user_id = :user_id AND t_users_scores.play_mode = :mode_num ORDER BY time DESC LIMIT 5;';
    $statement = $pdo -> prepare($query);
    $statement -> execute([':user_id' => $user_id, 'mode_num' => $mode_num]);
    while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
      $song_name = $row['song_name'];
      $beatmap_id = $row['beatmap_id'];
      $score = $row['score'];
      $mods = $row['mods'];
      $time = $row['time'];
      $rank = $row['rank'];
      print('<div class="ui left aligned">');
      print('<p>');
      print(get_datetime_diff($time).' - ');
      print('<a href="https://ripple.moe/b/'.$beatmap_id.'"> '.$song_name.'</a> ');
      print(number_format($score).' ('.$rank.') '.get_mods($mods));
      print('</p>');
      print('</div>');
    }
  }
  function print_users_most_passed_beatmaps($user_id, $mode_num) {
    $pdo = get_pdo();
    $query = 'SELECT COUNT(*) AS count, m_beatmaps.song_name, m_beatmaps.beatmap_id FROM t_users_scores INNER JOIN m_beatmaps ON t_users_scores.beatmap_md5 = m_beatmaps.beatmap_md5 WHERE t_users_scores.user_id = :user_id and t_users_scores.play_mode = :mode_num GROUP BY m_beatmaps.beatmap_md5 ORDER BY count DESC LIMIT 15';
    $statement = $pdo -> prepare($query);
    $statement -> execute([':user_id' => $user_id, 'mode_num' => $mode_num]);
    $font_size = 180;
    while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
      $count = $row['count'];
      $song_name = $row['song_name'];
      $beatmap_id = $row['beatmap_id'];
      print('<div class="ui left aligned">');
      print('<p style="font-size: '.$font_size.'%";>');
      print($count.' Plays - ');
      print('<a href="https://ripple.moe/b/'.$beatmap_id.'"> '.$song_name.'</a> ');
      print('</p>');
      print('</div>');
      $font_size = $font_size - 6;
    }
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
  function print_playcount_chart_label($date) {
    for ($i = 0; $i < count($date); $i++) {
      print('"'.$date[$i].'",');
    }
  }
  function print_playcount_chart_data($playcount) {
    for ($i = 0; $i < count($playcount); $i++) {
      print($playcount[$i].',');
    }
  }
  function print_replays_chart_label($date) {
    for ($i = 0; $i < count($date); $i++) {
      print('"'.$date[$i].'",');
    }
  }
  function print_replays_chart_data($replays) {
    for ($i = 0; $i < count($replays); $i++) {
      print($replays[$i].',');
    }
  }
  function get_mods($mods_num) {
    $mods = array();
    $bin  = decbin($mods_num);
    $bits = str_split($bin);
    $bits = array_reverse($bits);
    $bits = array_filter($bits);
    foreach ( $bits as $pos => $bit ) {
        $bits[$pos] = pow(2, $pos);
    }
    $bits = array_values($bits);
    foreach ($bits as $bit) {
      if ($bit == 16384) {
        if (($key = array_search('SD', $mods)) !== false) {
          unset($mods[$key]);
          array_push($mods, 'PF');
        }
      } else if ($bit == 512) {
        if (($key = array_search('DT', $mods)) !== false) {
          unset($mods[$key]);
          array_push($mods, 'NC');
        }
      } else {
        array_push($mods, get_mod_str($bit));
      }
    }
    $mods_str = '';
    foreach ($mods as $mod) {
      $mods_str = $mods_str.$mod;
      if (next($mods) == True) {
          $mods_str = $mods_str.',';
      }
    }
    return $mods_str;
  }
  function get_mod_str($mod_num) {
    if ($mod_num == 1) {return 'NF'; }
    else if ($mod_num == 2) {return 'EZ';}
    else if ($mod_num == 8) {return 'HD';}
    else if ($mod_num == 16) {return 'HR';}
    else if ($mod_num == 32) {return 'SD';}
    else if ($mod_num == 64) {return 'DT';}
    else if ($mod_num == 256) {return 'HT';}
    else if ($mod_num == 576) {return 'NC';}
    else if ($mod_num == 1024) {return 'FL';}
    else if ($mod_num == 4096) {return 'SO';}
  }
  function print_donor_badge($user_id) {
    $pdo = get_pdo();
    $query = 'SELECT COUNT(*) AS count FROM m_users_badges WHERE user_id = :user_id AND badge_id = 14';
    $statement = $pdo -> prepare($query);
    $statement -> execute([':user_id' => $user_id]);
    $row = $statement -> fetch(PDO::FETCH_ASSOC);
    $is_donor = $row['count'];
    if ($is_donor == 1) {
      print('<div class="ui label">');
      print('<i class="money icon"></i> Ripple Donor');
      print('</div>');
    }
  }
?>
