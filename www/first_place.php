<?php
  function printFirstPlaceStats($score_id, $rank, $song_name_full, $mods, $accuracy, $time, $pp) {
    print('<tr>');
    print('<td><img src="/images/'.$rank.'.png" width="12" height="15">'.$song_name_full.' ('.sprintf('%0.2f', $accuracy).'%)</td>');
    print('<td>'.sprintf('%0.2f', $pp).'pp</td>');
    print('</tr>');
    print('<tr>');
    print('<td>'.$time.'</td>');
    print('<td><a href="https://ripple.moe/web/replays/'.$score_id.'">★ Download</a></td>');
    print('</tr>');
/*
    print('<table>');
    print('<tbody><tr><td>');
    print('<div class="h">');
    print('<img src="/images/'.$rank.'.png" width="12" height="15">');
    print('<b>'.$song_name_full.' '.$mods.'</b> ('.sprintf('%0.2f', $accuracy).'%)');
    print('</div>');
    print('<div class="c">');
    print('<time>'.$time.'</time>');
    print('</div>');
    print('</td>');
    print('<td>');
    print('<div class="pp-display">');
    print('<b>'.round($pp).'pp</b>');
    print('</div>');
    print('<div class="pp-display-weight">');
    print('<a href="https://ripple.moe/web/replays/'.$score_id.'">★</a>');
    print('</div>');
    print('</td>');
    print('</tr></tbody></table>');
    */
  }

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

  $query = 'SELECT m_first_place.score_id AS score_id, m_first_place.mods AS mods, m_first_place.rank AS rank, m_first_place.time AS time, m_first_place.accuracy AS accuracy, m_first_place.pp AS pp, m_beatmaps.artist AS artist, m_beatmaps.title AS title, m_beatmaps.version AS version FROM m_first_place_std m_first_place INNER JOIN m_beatmaps_std m_beatmaps ON m_first_place.beatmap_md5 = m_beatmaps.file_md5 ORDER BY time DESC;';

  $statement = $pdo -> prepare($query);
  $statement -> execute();

  print('<table class="ui table score-table orange">');
  while ($row = $statement -> fetch(PDO::FETCH_ASSOC)) {
    $rank = $row['rank'];
    $artist = $row['artist'];
    $title = $row['title'];
    $version = $row['version'];
    $song_name_full = "$artist - $title [$version]";
    $mods = $row['mods'];
    $accuracy = $row['accuracy'];
    $time = $row['time'];
    $pp = $row['pp'];
    $score_id = $row['score_id'];
    printFirstPlaceStats($score_id, $rank, $song_name_full, $mods, $accuracy, $time, $pp);
  }
  print('</table>');
?>
