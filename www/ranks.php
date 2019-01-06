<?php
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

  $query = 'SELECT rank, COUNT(rank) AS count FROM m_users_scores GROUP BY rank';

  $statement = $pdo -> prepare($query);
  $statement -> execute();

  # Set selected data.
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
?>
<table align="center" width="400" cellspacing="0" cellpadding="0">
  <tbody>
    <tr>
      <td width="42"><img height="42" src="/images/SS.png"></td><td width="50"><?php print($count_ss) ?></td>
      <td width="42"><img height="42" src="/images/S.png"></td><td width="50"><?php print($count_s) ?></td>
      <td width="42"><img height="42" src="/images/A.png"></td><td width="50"><?php print($count_a) ?></td>
    </tr>
  </tbody>
</table>
