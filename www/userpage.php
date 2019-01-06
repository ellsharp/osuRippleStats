<?php require_once('./init_userpage.php') ?>
<!DOCTYPE html>
<head>
  <title><?php print($username); ?>'s profile</title>
  <link rel="stylesheet" type="text/css" href="./style.css">
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
            labels: [<?php print_label($date); ?>],
            datasets: [
            {
               label: "Performance Ranking",
               borderColor: 'rgb(255, 0, 0)',
               lineTension: 0, //<===追加
               fill: false,    //<===追加
               data: [<?php print_data($pp_rank); ?>],
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
      <?php print_activity(); ?>
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
  </div>
</body>
