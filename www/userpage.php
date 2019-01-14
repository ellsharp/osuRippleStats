<?php require_once('./functions.php') ?>
<?php
  if (isset($_GET['u'])) { $user_id = $_GET['u']; }
  if (isset($_GET['m'])) { $mode_num = $_GET['m']; }
  $users_stats = get_users_stats($user_id, $mode_num);
  $username = $users_stats['username'];
  $global_leaderboard_rank = get_users_pp_rank_history($user_id, $mode_num);
  $ranked_score = $users_stats['ranked_score'];
  $accuracy = $users_stats['accuracy'];
  $playcount = $users_stats['playcount'];
  $total_score = $users_stats['total_score'];
  $level = $users_stats['level'];
  $total_hits = $users_stats['total_hits'];
  $max_combo = get_users_max_combo($user_id, $mode_num);
  $replays_watched = $users_stats['replays_watched'];
  $ranks_count = get_users_ranks_count($user_id, $mode_num);
  $registered_on = $users_stats['registered_on'];
  $registered_on_relative = get_datetime_diff($registered_on);
  $latest_activity = $users_stats['latest_activity'];
  $latest_activity_relative = get_datetime_diff($latest_activity);
  $country = $users_stats['country'];
  $count_ss = $ranks_count['ss'];
  $count_s = $ranks_count['s'];
  $count_a = $ranks_count['a'];
?>
<html>
<head>
  <title><?php print($username); ?>'s Ripple Stats</title>
  <link rel="stylesheet" type="text/css" href="semantic/dist/semantic.min.css">
  <link rel="stylesheet" type="text/css" href="style.css">
  <script
    src="https://code.jquery.com/jquery-3.1.1.min.js"
    integrity="sha256-hVVnYaiADRTO2PzUGmuLJr8BLUSjGIZsDYGmIJLv2b8="
    crossorigin="anonymous"></script>
  <script src="semantic/dist/semantic.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.4.0/Chart.min.js"></script>
  <script>
    window.onLoad=$('#current-level').progress({
  percent: 22
});
  </script>
</head>
<body>
  <div class="ui container">
    <h1 class="ui header center aligned"><?php print($username); ?>'s Ripple Stats</h1>
    <div class="ui two column grid">
      <div class="four wide column segment">
        <div class="ui segment top attached center aligned">
          <img src="https://a.ripple.moe/<?php print($user_id);?>" width=128px height=128px />
        </div>
        <div class="ui attached segment center aligned">
          <h1><?php print($username); ?></h1>
          <i class="<?php print($country); ?> flag"></i>
          <div class="ui label">
            <i class="money icon"></i> Ripple Donor
          </div>
        </div>
        <div class="ui attached segment">
          <p><i class="circle check icon"></i> <?php print($registered_on_relative); ?></p>
          <p><i class="play icon"></i> <?php print($latest_activity_relative); ?></p>
        </div>
        <div class="ui attached segment center aligned">
          <i class="big mouse pointer icon"></i>
          <i class="big tablet icon"></i>
          <i class="big keyboard icon"></i>
          <i class="big hand point up icon"></i>
        </div>
      </div>
      <div class="twelve wide column segment">
      <div class="ui four item menu">
        <a class="item <?php if($mode_num == 0){ print('active'); } ?>" href="/userpage.php?u=<?php print($user_id); ?>&m=0">osu!</a>
        <a class="item <?php if($mode_num == 1){ print('active'); } ?>" href="/userpage.php?u=<?php print($user_id); ?>&m=1">Taiko</a>
        <a class="item <?php if($mode_num == 2){ print('active'); } ?>" href="/userpage.php?u=<?php print($user_id); ?>&m=2">CatchTheBeat</a>
        <a class="item <?php if($mode_num == 3){ print('active'); } ?>" href="/userpage.php?u=<?php print($user_id); ?>&m=3">osu!mania</a>
      </div>
        <div class="ui secondary inverted top attached segment">
          <p>General</p>
        </div>
        <div class="ui secondary attached segment">
          <p>
            Performance: <?php print(number_format($users_stats['pp'])); ?>pp (#<?php print(number_format($users_stats['global_leaderboard_rank'])); ?>)
            <a href="https://ripple.moe/leaderboard?mode=0&p=1&country=<?php print(mb_strtolower($users_stats['country'])); ?>">
              <i class="<?php print($country); ?> flag link"></i>
            </a>
            #<?php print(number_format($users_stats['country_leaderboard_rank'])); ?>
          </p>
        </div>
        <div class="ui attached segment">
          <canvas id="ppRankingChart"></canvas>
          <script>
            var ctx = document.getElementById("ppRankingChart").getContext('2d');
            var ppRankingChart = new Chart(ctx, {
              type: 'line',
              data: {
                 labels: [<?php print_pp_chart_label($global_leaderboard_rank[0]); ?>],
                 datasets: [
                 {
                    label: "Performance Ranking",
                    borderColor: 'rgb(255, 128, 0)',
                    lineTension: 0, //<===追加
                    fill: false,    //<===追加
                    data: [<?php print_pp_chart_data($global_leaderboard_rank[1]); ?>],
                 },
                 ]
              },
              options: {
                 responsive: true,
                 scales: {
                   xAxes: [{
                     display: true,
                     ticks: {
                        callback: function(value) {return ((value % 30) == 0)? value + 'days ago' : ''},
                     }
                   }],
                   yAxes: [{
                     display: true,
                     ticks: {
                       reverse: true
                     }
                   }]
                 },
                 elements: {
                   point: {
                     radius: 0
                   }
                 }
               }
             });
          </script>
        </div>
        <div class="ui secondary attached segment">
          <p>Recent Activity</p>
        </div>
        <div class="ui attached segment">
          <div class="ui two column grid">
            <?php print_users_activity($user_id, $username); ?>
          </div>
        </div>
        <div class="ui secondary attached segment">
          <p>Detail Stats</p>
        </div>
        <div class="ui attached segment">
          <p>Ranked Score: <?php print(number_format($ranked_score)) ?></p>
        </div>
        <div class="ui attached segment">
          <p>Hit Accuracy: <?php print(number_format($accuracy, 2).'%') ?></p>
        </div>
        <div class="ui attached segment">
          <p>Play Count: <?php print(number_format($playcount)) ?></p>
        </div>
        <div class="ui attached segment">
          <p>Total Score: <?php print(number_format($total_score)) ?></p>
        </div>
        <div class="ui attached segment">
          <p>Current Level: <?php print(number_format($level)) ?></p>
          <div class="ui indicating progress">
            <div class="bar">
              <div class="progress" data-percent="74" id="current-level">74%</div>
            </div>
          </div>
        </div>
        <div class="ui attached segment">
          <p>Total Hits: <?php print(number_format($total_hits)) ?></p>
        </div>
        <div class="ui attached segment">
          <p>Maximum Combo: <?php print(number_format($max_combo)) ?></p>
        </div>
        <div class="ui attached segment">
          <p>Replays Watched by Others: <?php print(number_format($replays_watched)) ?></p>
        </div>
        <div class="ui attached segment">
          <p>Ranks</p>
        </div>
        <div class="ui secondary inverted attached segment">
          <p>Top Ranks</p>
        </div>
        <div class="ui attached segment">
          <p>Best Performance</p>
          <div class="ui top attached segment">
            a
          </div>
          <div class="ui attached segment">
          </div>
          <div class="ui bottom attached segment">
          </div>
          <p>First Place Ranks</p>
          <?php print_first_place_ranks($user_id, $mode_num); ?>
        </div>
        <div class="ui secondary inverted attached segment">
          <p>Historical</p>
        </div>
        <div class="ui secondary attached segment">
          <p>Play History</p>
        </div>
        <div class="ui attached segment">
          <canvas id="ChartDemo2" height="80px"></canvas>
          <script>
            var ctx = document.getElementById("ChartDemo2").getContext('2d');
            var ChartDemo = new Chart(ctx, {
               type: 'line',
               data: {
                  labels: ["Item1", "Item2", "Item3", "Item4", "Item5", "Item6", "Item7"],
                  datasets: [
                  {
                     label: "Chart-1",
                     borderColor: 'rgb(255, 0, 0)',
                     lineTension: 0,
                     fill: false,
                     data: [20, 26, 12, 43, 33, 21, 29],
                  },
                  ]
               },
               options: {
                  responsive: true,
               }
            });
          </script>
        </div>
        <div class="ui secondary attached segment">
          <p>Most Passed Beatmaps</p>
        </div>
        <div class="ui attached segment">
          <?php print_users_most_passed_beatmaps($user_id, $mode_num); ?>
        </div>
        <div class="ui secondary attached segment">
          <p>Recent Plays</p>
        </div>
        <div class="ui attached segment">
          <?php print_users_recent_plays($user_id, $mode_num); ?>
        </div>
        <div class="ui secondary attached segment">
          <p>Replays Watched History</p>
        </div>
        <div class="ui attached segment">
          <canvas id="ChartDemo3" height="80px"></canvas>
          <script>
            var ctx = document.getElementById("ChartDemo3").getContext('2d');
            var ChartDemo = new Chart(ctx, {
               type: 'line',
               data: {
                  labels: ["Item1", "Item2", "Item3", "Item4", "Item5", "Item6", "Item7"],
                  datasets: [
                  {
                     label: "Chart-1",
                     borderColor: 'rgb(255, 0, 0)',
                     lineTension: 0,
                     fill: false,
                     data: [20, 26, 12, 43, 33, 21, 29],
                  },
                  ]
               },
               options: {
                  responsive: true,
               }
            });
          </script>
        </div>
        <div class="ui secondary inverted attached segment">
          <p>Achievements</p>
        </div>
        <div class="ui bottom attached segment">
        </div>
      </div>
    </div>
  </div>
</body>
</html>
