<?php
  require_once './functions.php';
  require_logined_session();

  if (! validate_token(filter_input(INPUT_GET, 'token'))) {
    header('Content-Type: text/plain; charset=UTF-8', true, 400);
    exit('Invalid token');
  }

  setcookie(session_name(), '', 1);
  session_destroy();
  header('Location: /manage/login.php');
?>
