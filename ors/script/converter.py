from ors.script import converter
from datetime import datetime
import pytz

def convert_users_score(user_id, users_score):
    score = {}
    score['user_id'] = user_id
    score['score_id'] = users_score['id']
    score['beatmap_md5'] = users_score['beatmap_md5']
    score['max_combo'] = users_score['max_combo']
    score['score'] = users_score['score']
    score['is_full_combo'] = int(users_score['full_combo'])
    score['mods'] = users_score['mods']
    score['count_300'] = users_score['count_300']
    score['count_100'] = users_score['count_100']
    score['count_50'] = users_score['count_50']
    score['count_geki'] = users_score['count_geki']
    score['count_katu'] = users_score['count_katu']
    score['count_miss'] = users_score['count_miss']
    score['time'] = convert_datetime(convert_iso_datetime(users_score['time']))
    score['play_mode'] = users_score['play_mode']
    score['accuracy'] = users_score['accuracy']
    score['pp'] = users_score['pp']
    score['rank'] = users_score['rank']
    score['completed'] = users_score['completed']
    score['created_on'] = convert_datetime(datetime.now(pytz.timezone('UTC')))
    return score

def convert_users_stats(users_stats):
    modes = ['std', 'taiko', 'ctb', 'mania']
    stats = {}
    stats['user_id'] = users_stats['id']
    stats['username'] = users_stats['username']
    stats['username_aka'] = users_stats['username_aka']
    stats['registered_on'] = convert_datetime(convert_iso_datetime(users_stats['registered_on']))
    stats['privileges'] = users_stats['privileges']
    stats['latest_activity'] = convert_datetime(convert_iso_datetime(users_stats['latest_activity']))
    stats['country'] = users_stats['country']
    for mode in modes:
        stats['ranked_score_' + mode] = users_stats[mode]['ranked_score']
        stats['total_score_' + mode] = users_stats[mode]['total_score']
        stats['playcount_' + mode] = users_stats[mode]['playcount']
        stats['replays_watched_' + mode] = users_stats[mode]['replays_watched']
        stats['total_hits_' + mode] = users_stats[mode]['total_hits']
        stats['level_' + mode] = users_stats[mode]['level']
        stats['accuracy_' + mode] = users_stats[mode]['accuracy']
        stats['pp_' + mode] = users_stats[mode]['pp']
        if users_stats[mode]['global_leaderboard_rank'] == None:
            stats['global_leaderboard_rank_' + mode] = 0
        else:
            stats['global_leaderboard_rank_' + mode] = users_stats[mode]['global_leaderboard_rank']
        if users_stats[mode]['country_leaderboard_rank'] == None:
            stats['country_leaderboard_rank_' + mode] = 0
        else:
            stats['country_leaderboard_rank_' + mode] = users_stats[mode]['country_leaderboard_rank']
    stats['play_style'] = users_stats['play_style']
    stats['favourite_mode'] = users_stats['favourite_mode']
    stats['created_on'] = convert_datetime(datetime.now(pytz.timezone('UTC')))
    return stats

def convert_users_badge(user_id, users_badge):
    badge = {}
    badge['user_id'] = user_id
    badge['badge_id'] = users_badge['id']
    badge['name'] = users_badge['name']
    badge['icon'] = users_badge['icon']
    badge['created_on'] = convert_datetime(datetime.now(pytz.timezone('UTC')))
    return badge

def convert_users_silence_info(user_id, users_silence_info):
    silence_info = {}
    silence_info['user_id'] = user_id
    silence_info['reason'] = users_silence_info['reason']
    silence_info['end'] = convert_datetime(convert_iso_datetime(users_silence_info['end']))
    silence_info['created_on'] = convert_datetime(datetime.now(pytz.timezone('UTC')))
    return silence_info

def convert_beatmap(beatmap, mode):
    beatmap_temp = {}
    beatmap_temp['beatmap_id'] = beatmap['beatmap_id']
    beatmap_temp['beatmapset_id'] = beatmap['beatmapset_id']
    beatmap_temp['beatmap_md5'] = beatmap['beatmap_md5']
    beatmap_temp['song_name'] = beatmap['song_name'].replace('\'', '\\\'')
    beatmap_temp['ar'] = beatmap['ar']
    beatmap_temp['od'] = beatmap['od']
    beatmap_temp['difficulty'] = beatmap['difficulty']
    beatmap_temp['max_combo'] = beatmap['max_combo']
    beatmap_temp['hit_length'] = beatmap['hit_length']
    beatmap_temp['ranked'] = beatmap['ranked']
    beatmap_temp['ranked_status_frozen'] = beatmap['ranked_status_frozen']
    beatmap_temp['latest_update'] = convert_datetime(convert_iso_datetime(beatmap['latest_update']))
    beatmap_temp['mode'] = mode
    beatmap_temp['created_on'] = convert_datetime(datetime.now(pytz.timezone('UTC')))
    return beatmap_temp

def convert_activity(score, beatmap_id, song_name, ranking):
    activity = {}
    activity['user_id'] = score['user_id']
    activity['score_id'] = score['score_id']
    activity['score'] = score['score']
    activity['beatmap_id'] = beatmap_id
    activity['beatmap_md5'] = score['beatmap_md5']
    activity['song_name'] = song_name.replace('\'', '\\\'')
    activity['ranking'] = ranking
    if ranking == 1:
        activity['type'] = 1
    elif ranking == -1:
        activity['type'] = 2
    else:
        activity['type'] = 0
    activity['mode'] = score['play_mode']
    activity['rank'] = score['rank']
    activity['archive_on'] = score['time']
    activity['created_on'] = convert_datetime(datetime.now(pytz.timezone('UTC')))
    return activity

def convert_beatmap_peppy(beatmap_info_peppy):
    beatmap_info = {}
    beatmap_info['beatmap_id'] = beatmap_info_peppy['beatmap_id']
    beatmap_info['beatmapset_id'] = beatmap_info_peppy['beatmapset_id']
    beatmap_info['beatmap_md5'] = beatmap_info_peppy['file_md5']
    song_name = beatmap_info_peppy['artist'] + ' - ' + beatmap_info_peppy['title'] + ' [' + beatmap_info_peppy['version'] + ']'
    beatmap_info['song_name'] = song_name.replace('\'', '\\\'')
    beatmap_info['ar'] = beatmap_info_peppy['diff_approach']
    beatmap_info['od'] = beatmap_info_peppy['diff_overall']
    beatmap_info['difficulty'] = beatmap_info_peppy['difficultyrating']
    beatmap_info['max_combo'] = beatmap_info_peppy['max_combo']
    beatmap_info['hit_length'] = beatmap_info_peppy['hit_length']
    beatmap_info['ranked'] = -1
    beatmap_info['ranked_status_frozen'] = -1
    beatmap_info['latest_update'] = beatmap_info_peppy['last_update']
    beatmap_info['mode'] = beatmap_info_peppy['mode']
    beatmap_info['created_on'] = convert_datetime(datetime.now(pytz.timezone('UTC')))
    return beatmap_info

def convert_first_place_score(first_place_score):
    first_place_score['time'] = convert_datetime(convert_iso_datetime(first_place_score['time']))
    return first_place_score

def convert_iso_datetime(iso_str):
    dt = None
    if ":" == iso_str[-3:-2]:
        iso_str = iso_str[:-3]+iso_str[-2:]
    try:
        dt = datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%S%Z')
        dt = pytz.utc.localize(dt).astimezone(pytz.timezone('UTC'))
    except ValueError:
        try:
            dt = datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%S%z')
            dt = dt.astimezone(pytz.timezone('UTC'))
        except ValueError:
            pass
    return dt

def convert_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')
