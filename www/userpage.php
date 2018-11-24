<!DOCTYPE html>
<head>
  <title>XXX's profile</title>
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
    div.performance-chart {
      padding: 10px;
    }
    div.activity {
      padding: 10px;
      font-size: 12px;
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
    <div class="username">ellsharp</div>
  </div>
  <div class="profile-right">
    <div class="general">General</div>
    <div class="section">
      <b>Performance: 3,000pp (#2,000)</b>
      <a href="https://ripple.moe/leaderboard?mode=0&p=1&country=jp"><img src="https://s.ppy.sh/images/flags/jp.gif" /></a> #100
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
    </div>
  </div>
</body>
