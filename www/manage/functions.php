<?php
  function require_unlogined_session() {
    @session_start();
    if (isset($_SESSION['username'])) {
      header('Location: /manage/portal.php');
      exit;
    }
  }

  function require_logined_session() {
    @session_start();
    if (! isset($_SESSION['username'])) {
      header('Location: /manage/login.php');
      exit;
    }
  }

  function generate_token() {
    return hash('sha256', session_id());
  }

  function validate_token($token) {
    return $token === generate_token();
  }

  function h($str) {
    return htmlspecialchars($str, ENT_QUOTES, 'UTF-8');
  }

  function get_pdo(){
    $database_config = parse_ini_file('../../conf/database.conf');
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

  function execute_score_search($score_id) {
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

  function execute_beatmap_search_md5($beatmap_md5) {
    $pdo = get_pdo();
    $query = 'SELECT * FROM m_beatmaps WHERE beatmap_md5 = :beatmap_md5';
    $statement = $pdo -> prepare($query);
    $statement -> execute([':beatmap_md5' => $beatmap_md5]);
    $beatmap_data = ($row = $statement -> fetch(PDO::FETCH_ASSOC));
    if ($beatmap_data) {
      print('<table class="ui celled table">');
      print('<thead>');
      foreach ($beatmap_data as $key => $value) {
        print('<tr><td>'.$key.'</td><td>'.$value.'</td></tr>');
      }
      print('</thead>');
      print('</table>');
    } else {
      print('<b>beatmap_md5 not found.</b>');
    }
  }

  function execute_beatmap_search_id($beatmap_id) {
    $pdo = get_pdo();
    $query = 'SELECT * FROM m_beatmaps WHERE beatmap_id = :beatmap_id';
    $statement = $pdo -> prepare($query);
    $statement -> execute([':beatmap_id' => $beatmap_id]);
    $beatmap_data = ($row = $statement -> fetch(PDO::FETCH_ASSOC));
    if ($beatmap_data) {
      print('<table class="ui celled table">');
      print('<thead>');
      foreach ($beatmap_data as $key => $value) {
        print('<tr><td>'.$key.'</td><td>'.$value.'</td></tr>');
      }
      print('</thead>');
      print('</table>');
    } else {
      print('<b>beatmap_id not found.</b>');
    }
  }

  function execute_user_search_id($user_id) {
    $pdo = get_pdo();
    $query = 'SELECT * FROM m_users_stats WHERE user_id = :user_id';
    $statement = $pdo -> prepare($query);
    $statement -> execute([':user_id' => $user_id]);
    $user_data = ($row = $statement -> fetch(PDO::FETCH_ASSOC));
    if ($user_data) {
      print('<table class="ui celled table">');
      print('<thead>');
      foreach ($user_data as $key => $value) {
        print('<tr><td>'.$key.'</td><td>'.$value.'</td></tr>');
      }
      print('</thead>');
      print('</table>');
    } else {
      print('<b>user_id not found.</b>');
    }
  }

  function execute_user_search_name($username) {
    $pdo = get_pdo();
    $query = 'SELECT * FROM m_users_stats WHERE username = :username';
    $statement = $pdo -> prepare($query);
    $statement -> execute([':username' => $username]);
    $user_data = ($row = $statement -> fetch(PDO::FETCH_ASSOC));
    if ($user_data) {
      print('<table class="ui celled table">');
      print('<thead>');
      foreach ($user_data as $key => $value) {
        print('<tr><td>'.$key.'</td><td>'.$value.'</td></tr>');
      }
      print('</thead>');
      print('</table>');
    } else {
      print('<b>username not found.</b>');
    }
  }
?>
