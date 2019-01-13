<?php
  function printFirstPlaceStats($score_id, $beatmap_id, $rank, $song_name, $mods, $accuracy, $time, $pp) {
    print('<tr>');
    print('<td><img src="/images/'.$rank.'.png" width="12" height="15" style="padding-right: 8px"><a href="https://ripple.moe/b/'.$beatmap_id.'">'.$song_name.' ('.sprintf('%0.2f', $accuracy).'%)</a></td>');
    print('<td style="text-align: right">'.sprintf('%d', $pp).'pp</td>');
    print('</tr>');
    print('<tr>');
    print('<td>'.$time.'</td>');
    print('<td style="text-align: right"><a href="https://ripple.moe/web/replays/'.$score_id.'">★</a></td>');
    print('</tr>');
  }

  function decToBits($dec) {
    $bin  = decbin($dec);
    $bits = str_split($bin);
    $bits = array_reverse($bits);
    $bits = array_filter($bits);

    foreach ( $bits as $pos => $bit ) {
        $bits[$pos] = pow(2, $pos);
    }

    $bits = array_values($bits);

    return $bits;
  }
  print(var_dump(decToBits(17456)));

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

  $query = 'SELECT m_first_place.score_id AS score_id, m_first_place.mods AS mods, m_first_place.rank AS rank, m_first_place.time AS time, m_first_place.accuracy AS accuracy, m_first_place.pp AS pp, m_beatmaps.song_name, m_beatmaps.beatmap_id as beatmap_id FROM m_first_place INNER JOIN  m_beatmaps ON m_first_place.beatmap_md5 = m_beatmaps.beatmap_md5 ORDER BY time DESC;';

  $statement = $pdo -> prepare($query);
  $statement -> execute();

  print('<table class="ui table score-table orange">');
  while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
    $rank = $row['rank'];
    $song_name_full = $row['song_name'];
    $mods = $row['mods'];
    $accuracy = $row['accuracy'];
    $time = $row['time'];
    $pp = $row['pp'];
    $score_id = $row['score_id'];
    $beatmap_id = $row['beatmap_id'];
    printFirstPlaceStats($score_id, $beatmap_id, $rank, $song_name_full, $mods, $accuracy, $time, $pp);
  }
  print('</table>');
?>
