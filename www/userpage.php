<?php require_once('./functions.php') ?>
<?php require_once('./init_userpage.php') ?>
<?php
  if (isset($_GET['u'])) { $user_id = $_GET['u']; }
  if (isset($_GET['m'])) { $mode_num = $_GET['m']; }
  $users_stats = get_users_stats($user_id, $mode_num);
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
  $count_ss = $ranks_count['ss'];
  $count_s = $ranks_count['s'];
  $count_a = $ranks_count['a'];
?>
<!DOCTYPE html>
<head>
  <title><?php print($users_stats['username']); ?>'s profile</title>
  <link rel="stylesheet" type="text/css" href="./style.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.4.0/Chart.min.js"></script>
  <script
  src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
  integrity="sha256-3edrmyuQ0w65f8gfBsqowzjJe2iM6n0nKciPUp8y+7E="
  crossorigin="anonymous"></script>
  <script type='text/javascript'>
  jQuery(function($) {
    var nav = $('div.profile-left'),
    offset = nav.offset();
    $(window).scroll(function () {
      if($(window).scrollTop() > offset.top) {
        nav.addClass('fixed');
      } else {
        nav.removeClass('fixed');
      }
    });
  });
  </script>

</head>
<body>
  <h1><?php print($users_stats['username'].'\'s Userpage'); ?></h1>
  <div class="profile-left">
    <div class="avatar"><img src="https://a.ripple.moe/<?php print($users_stats['user_id']); ?>" class="avatar" /></div>
    <div class="username"><?php print($users_stats['username']); ?></div>
  </div>
  <div class="profile-right">
    <div class="general">General</div>
    <div class="section">
      <b>Performance: <?php print(number_format($users_stats['pp'])); ?>pp (#<?php print(number_format($users_stats['global_leaderboard_rank'])); ?>)</b>
      <a href="https://ripple.moe/leaderboard?mode=0&p=1&country=<?php print(mb_strtolower($users_stats['country'])); ?>">
        <img src="https://s.ppy.sh/images/flags/<?php print(mb_strtolower($users_stats['country'])); ?>.gif" />
      </a>
      #<?php print(number_format($users_stats['country_leaderboard_rank'])); ?>
    </div>
    <div class="performance-chart">
      <canvas id="ChartDemo" width="600" height="200"></canvas>
      <script type="text/javascript">
      var ctx = document.getElementById("ChartDemo").getContext('2d');
      var ChartDemo = new Chart(ctx, {
         type: 'line',
         data: {
            labels: [<?php print_label($global_leaderboard_rank[0]); ?>],
            datasets: [
            {
               label: "Performance Ranking",
               borderColor: 'rgb(255, 0, 0)',
               lineTension: 0, //<===追加
               fill: false,    //<===追加
               data: [<?php print_data($global_leaderboard_rank[1]); ?>],
            },
            ]
         },
         options: {
            responsive: false,
            scales: {
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
    <div class="section">Recent Activity</div>
    <div class="activity">
      <table>
      <?php print_users_activity($user_id, $mode_num); ?>
      </table>
    </div>
    <div class="section">Detail Stats</div>
    <div class="stats"><b>Ranked Score:</b> <?php print(number_format($ranked_score)) ?></div>
    <div class="blank"></div>
    <div class="stats"><b>Hit Accuracy:</b> <?php print(number_format($accuracy, 2).'%') ?></div>
    <div class="blank"></div>
    <div class="stats"><b>Play Count:</b> <?php print(number_format($playcount)) ?></div>
    <div class="blank"></div>
    <div class="stats"><b>Total Score:</b> <?php print(number_format($total_score)) ?></div>
    <div class="blank"></div>
    <div class="stats"><b>Current Level:</b> <?php print(number_format($level)) ?></div>
    <div class="blank"></div>
    <div class="stats"><b>Total Hits:</b> <?php print(number_format($total_hits)) ?></div>
    <div class="blank"></div>
    <div class="stats"><b>Maximum Combo:</b> <?php print(number_format($max_combo)) ?></div>
    <div class="blank"></div>
    <div class="stats"><b>Replays Watched by Others:</b> <?php print(number_format($replays_watched)) ?></div>
    <div class="blank"></div>
    <div class="stats"><b>Ranks</b></div>
    <div class="ranks">
      <table align="center" width="400" cellspacing="0" cellpadding="0">
        <tbody>
          <tr>
            <td width="42"><img height="42" src="/images/SS.png"></td><td width="50"><?php print($count_ss) ?></td>
            <td width="42"><img height="42" src="/images/S.png"></td><td width="50"><?php print($count_s) ?></td>
            <td width="42"><img height="42" src="/images/A.png"></td><td width="50"><?php print($count_a) ?></td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="stats"><b>Top Ranks</b></div>
    <div class="best-performance">
      Best Performance
    </div>
    <div class="first-place-ranks">
      First Place Ranks
      <table class="ui table score-table orange" style="border: 1px; border-color: #000000">
        <?php print_first_place_ranks($user_id, $mode_num); ?>
      </table>
    </div>
  </div>
</body>
