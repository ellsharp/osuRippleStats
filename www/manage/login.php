<?php
  require_once './functions.php';
  require_unlogined_session();

  $hashes = [
    'orsmng' => '$2y$10$xMWxxPRjm5joUpIMr7Pr6.P2jtMWC4I5Y.mXEQ89/HOstOHbdwvE.',
  ];

  $username = filter_input(INPUT_POST, 'username');
  $password = filter_input(INPUT_POST, 'password');
  if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (
        validate_token(filter_input(INPUT_POST, 'token')) &&
        password_verify(
          $password,
          isset($hashes[$username])
            ? $hashes[$username]
            : 'ripple'
        )
    ) {
      session_regenerate_id(true);
      $_SESSION['username'] = $username;
      header('Location: /manage/portal.php');
    }
    http_response_code(403);
  }
  header('Content-Type: text/html; charset=UTF-8');
?>
<!DOCTYPE html>
<html>
<head>
<title>Login</title>
<link rel="stylesheet" type="text/css" href="/semantic/dist/semantic.min.css">
<script
  src="https://code.jquery.com/jquery-3.1.1.min.js"
  integrity="sha256-hVVnYaiADRTO2PzUGmuLJr8BLUSjGIZsDYGmIJLv2b8="
  crossorigin="anonymous"></script>
<script src="/semantic/dist/semantic.min.js"></script>
</head>
<body>
  <div class="ui container" style="padding-top: 10em;">
    <h1 class="ui header center aligned" style="padding-bottom: 2em;">ORS Management Portal</h1>
    <div class="ui grid">
      <div class="five wide column"></div>
      <div class="six wide column">
        <?php if (http_response_code() === 403): ?>
          <div class="ui error message">
            <div class="header">
              Login failed.
            </div>
            <p>Invalid username or password.</p>
          </div>
        <?php endif; ?>
        <div class="ui segment center aligned">
          <form class="ui form" method="post" action="">
            <div class="field">
              <input type="text" name="username" value="" placeholder="Username">
            </div>
            <div class="field">
              <input type="password" name="password" value="" placeholder="Password">
            </div>
            <div class="field">
              <input type="hidden" name="token" value="<?=h(generate_token()) ?>">
            </div>
            <div class="field">
              <button class="ui button center aligned" type="submit">Login</button>
            </div>
          </form>
        </div>
      </div>
      <div class="five wide column"></div>
    </div>
  </div>
</body>
</html>
