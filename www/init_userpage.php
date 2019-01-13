<?php


  function print_label($date) {
    for ($i = 0; $i < count($date); $i++) {
      if ($i == 29) {
        print('"ALOHA", ');
      } else {
        print('"", ');
        //print($date[$i].',');
      }
    }
  }
  function print_data($pp_rank) {
    for ($i = 0; $i < count($pp_rank); $i++) {
      print($pp_rank[$i].',');
    }
  }
  /*
  function print_activity() {
      if ($type != 2) {
        if ($ranking < 51) {
          print('<tr>');
          print('<td class="activity-time">'.get_datetime_diff($archived_on).'</td>');
          print('<td class="activity-detail">');
          print('<img src="/images/'.$rank.'_small.png" />');
          print('ellsharp archived rank #'.$ranking.' on <a href="https://ripple.moe/b/'.$beatmap_id.'">'.$song_name.'</a> ('.get_gamemode($mode).')');
          print('</td>');
          print('<tr>');
        }
      } else if ($type == 2) {
        print('<tr>');
        print('<td class="activity-time">'.get_datetime_diff($archived_on).'</td>');
        print('<td class="activity-detail">');
        print('ellsharp has lost first place on on <a href="https://ripple.moe/b/'.$beatmap_id.'">'.$song_name.'</a> ('.get_gamemode($mode).')');
        print('</td>');
        print('<tr>');
      }
      $counter++;
      if ($counter > 151) {
        break;
      }
    }
  */
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
?>
