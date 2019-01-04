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
    $ranked_score_std = $row['ranked_score_std'];
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
      print('<tr>');
      print('<td class="activity-time">'.get_datetime_diff($archived_on).'</td>');
      if ($type != 2) {
        if ($ranking < 51) {
          print('<td class="activity-detail">');
          print('<img src="/images/'.$rank.'_small.png" />');
          print('ellsharp archived rank #'.$ranking.' on <a href="https://ripple.moe/b/'.$beatmap_id.'">'.$song_name.'</a> ('.get_gamemode($mode).')');
          print('</td>');
        }
      }
      print('<tr>');
      $counter++;
      if ($counter > 30) {
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
<!DOCTYPE html>
<head>
  <title><?php print($username); ?>'s profile</title>
  <style type="text/css">
    body {
      margin-right: auto;
      margin-left: auto;
      width: 860px;
    }
    div.profile-left {
      width: 220px;
      float: left;
      background-color: #FF0000
    }
    div.profile-right {
      width: 640px;
      float: left;
      background-color: #00FF00
    }
    div.avatar {
      padding-top: 46px;
      padding-left: 46px;
      padding-right: 46px;
    }
    div.username {
      font-size: 24px;
      text-align: center;
    }
    div.general {
      background-color: #444444;
      color: #FFFFFF
    }
    div.section {
      background-color: #CCCCCC;
      color: #000000;
    }
    div.stats {
      background-color: #EEEEEE;
      color: #000000;
    }
    div.performance-chart {
      padding: 10px;
    }
    div.activity {
      padding: 10px;
      font-size: 10px;
    }
    td.activity-time {
      width: 120px;
    }
    td.activity-detail {
      width: 500px;
    }
    img.avatar {
      width: 128px;
      height: 128px;
    }
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.4.0/Chart.min.js"></script>
</head>
<body>
  <h1>It works</h1>
  <div class="profile-left">
    <div class="avatar"><img src="https://a.ripple.moe/70666" class="avatar" /></div>
    <div class="username"><?php print($username); ?></div>
  </div>
  <div class="profile-right">
    <div class="general">General</div>
    <div class="section">
      <b>Performance: <?php print(number_format($pp_std)); ?>pp (#<?php print(number_format($global_leaderboard_rank_std)); ?>)</b>
      <a href="https://ripple.moe/leaderboard?mode=0&p=1&country=jp"><img src="https://s.ppy.sh/images/flags/jp.gif" /></a> #<?php print(number_format($country_leaderboard_rank_std)); ?>
    </div>
    <div class="performance-chart">
      <canvas id="ChartDemo" width="600" height="200"></canvas>
      <script type="text/javascript">
      var ctx = document.getElementById("ChartDemo").getContext('2d');
      var ChartDemo = new Chart(ctx, {
         type: 'line',
         data: {
            labels: ["Item1", "Item2", "Item3", "Item4", "Item5", "Item6", "Item7"],
            datasets: [
            {
               label: "Chart-1",
               borderColor: 'rgb(255, 0, 0)',
               lineTension: 0, //<===追加
               fill: false,    //<===追加
               data: [20, 26, 12, 43, 33, 21, 29],
            },
            ]
         },
         options: {
            responsive: false,
         }
        });
      </script>
    </div>
    <div class="section">Recent Activity</div>
    <div class="activity">
      <table>
        <tr>
          <td class="activity-time">about 2 hours ago</td>
          <td class="activity-detail">adadada</td>
        </tr>
        <tr>
          <td class="activity-time">about 2 hours ago</td>
          <td class="activity-detail">bababababa</td>
        </tr>
      </table>
      <table>
      <?php print_activity(); ?>
      </table>
    </div>
    <div class="section">Detail Stats</div>
    <div class="stats">Ranked Score: <?php print(number_format($ranked_score_std)) ?></div>
  </div>
</body>
