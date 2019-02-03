<?php require_once('./functions.php') ?>
<?php
  if (isset($_GET['score-id'])) {
    $score_id = $_GET['score-id'];
  } else {
    $score_id = null;
  }
  function print_score_id_detail($score_id) {
    if ($score_id != null) {
      $pdo = get_pdo();
      $query = 'SELECT * FROM t_users_scores INNER JOIN m_beatmaps ON t_users_scores.beatmap_md5 = m_beatmaps.beatmap_md5 WHERE score_id = :score_id';
      $statement = $pdo -> prepare($query);
      $statement -> execute([':score_id' => $score_id]);
      $score_data = ($row = $statement -> fetch(PDO::FETCH_ASSOC));
      if ($score_data) {
        $user_id = $score_data['user_id'];
        $score_id = $score_data['score_id'];
        $mods = $score_data['mods'];
        $rank = $score_data['rank'];
        $time = $score_data['time'];
        $accuracy = $score_data['accuracy'];
        $pp = $score_data['pp'];
        print('<table class="ui celled table">');
        print('<thead>');
        foreach ($score_data as $key => $value) {
          print('<tr><td>'.$key.'</td><td>'.$value.'</td></tr>');
        }
        print('</thead>');
        print('</table>');
      } else {
        print('<b>score_id not found.</b>');
      }
    }
  }
?>
<html>
<head>
  <title>ORS Score Search</title>
  <link rel="stylesheet" type="text/css" href="semantic/dist/semantic.min.css">
  <script src="semantic/dist/semantic.min.js"></script>
</head>
<body>
  <div class="ui grid">
    <div class="four wide column"></div>
      <div class="eight wide column">
        <form class="ui form">
          <div class="field">
            <label>score_id</label>
            <input type="text" name="score-id" placeholder="Enter score_id">
          </div>
          <button class="ui button" type="submit">Search</button>
        </form>
      <?php print_score_id_detail($score_id) ?>
      </div>
    <div class="four wide column"></div>
  </div>
</html>
