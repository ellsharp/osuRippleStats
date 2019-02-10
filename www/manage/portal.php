<?php
  require_once './functions.php';
  require_logined_session();
  header('Content-Type: text/html; charset=UTF-8');
?>
<html>
<head>
  <title>ORS Management Portal</title>
  <link rel="stylesheet" type="text/css" href="/semantic/dist/semantic.min.css">
  <script src="/semantic/dist/semantic.min.js"></script>
</head>
<body>
  <div class="ui container">
    <div class="ui menu">
      <div class="right item">
        <h1 class="ui header center aligned">ORS Management Portal</h1>
      </div>
      <div class="right item">
        <a href="/manage/logout.php?token=<?=h(generate_token()) ?>">
          <div class="ui button">Log out</div>
        </a>
      </div>
    </div>
    <div class="ui three column relaxed grid">
      <div class="column">
        <div class="ui red attached center aligned segment">
          <div class="ui large header">
            <i class="tiny newspaper outline icon"></i>Score
          </div>
        </div>
        <div class="ui attached segment">
          <form class="ui form" method="post" action="/manage/portal.php">
            <div class="ui fluid icon input">
              <input type="text" name="score_id" value="" placeholder="score_id">
              <i class="search icon"></i>
            </div>
          </form>
        </div>
      </div>
      <div class="column">
        <div class="ui blue attached center aligned segment">
          <div class="ui large header">
            <i class="tiny music icon"></i>Beatmap
          </div>
        </div>
        <div class="ui attached segment">
          <form class="ui form" method="post" action="/manage/portal.php">
            <div class="ui fluid icon input">
              <input type="text" name="beatmap_md5" value="" placeholder="beatmap_md5">
              <i class="search icon"></i>
            </div>
          </form>
        </div>
        <div class="ui attached segment">
          <form class="ui form" method="post"action="/manage/portal.php">
            <div class="ui fluid icon input">
              <input type="text" name="beatmap_id" value="" placeholder="beatmap_id">
              <i class="search icon"></i>
            </div>
          </form>
        </div>
      </div>
      <div class="column">
        <div class="ui green attached center aligned segment">
          <div class="ui large header">
            <i class="tiny user icon"></i>User
          </div>
        </div>
        <div class="ui attached segment">
          <form class="ui form" method="post" action="/manage/portal.php">
            <div class="ui fluid icon input">
              <input type="text" name="user_id" value="" placeholder="user_id">
              <i class="search icon"></i>
            </div>
          </form>
        </div>
        <div class="ui attached segment">
          <form class="ui form" method="post" action="/manage/portal.php">
            <div class="ui fluid icon input">
              <input type="text" name="username" value="" placeholder="username">
              <i class="search icon"></i>
            </div>
          </form>
        </div>
      </div>
    </div>
    <?php if (isset($_POST['score_id'])): ?>
      <div class="ui red segment">
        <div class="ui header">Search Result</div>
        <?php execute_score_search($_POST['score_id']); ?>
      </div>
    <?php endif; ?>
    <?php if (isset($_POST['beatmap_md5'])): ?>
      <div class="ui blue segment">
        <div class="ui header">Search Result</div>
        <?php execute_beatmap_search_md5($_POST['beatmap_md5']); ?>
      </div>
    <?php endif; ?>
    <?php if (isset($_POST['beatmap_id'])): ?>
      <div class="ui blue segment">
        <div class="ui header">Search Result</div>
        <?php execute_beatmap_search_id($_POST['beatmap_id']); ?>
      </div>
    <?php endif; ?>
    <?php if (isset($_POST['user_id'])): ?>
      <div class="ui green segment">
        <div class="ui header">Search Result</div>
        <?php execute_user_search_id($_POST['user_id']); ?>
      </div>
    <?php endif; ?>
    <?php if (isset($_POST['username'])): ?>
      <div class="ui green segment">
        <div class="ui header">Search Result</div>
        <?php execute_user_search_name($_POST['username']); ?>
      </div>
    <?php endif; ?>
  </div>
</html>
