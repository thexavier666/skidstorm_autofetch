#!/usr/bin/env python3

import json
import requests
import threading
import time
import os
import bottle
import sys
import datetime

from itertools import islice

from config_dir import config
from config_dir import config_html

def get_clan_rank():

    player_full_db = config.player_full_db_file
    if os.path.exists(player_full_db) == False:
        return get_static_page('error.html')

    clan_id_dict = config.clan_id_single_dict

    col_header = ['rank','clan_tag','clan_name','clan_score']
    clan_rank_list = []

    for key in clan_id_dict:

        tmp_list = [ \
                0,
                clan_id_dict[key]['clan_tag'],
                clan_id_dict[key]['clan_name'],
                get_clan_score(key,'public',True)]

        clan_rank_list.append(tmp_list)

    clan_rank_list = clan_rank_list[0:10]

    sorted_clan_rank_list = sorted(clan_rank_list, key = lambda x:x[3], reverse=True)

    init_pos = 1
    for row in sorted_clan_rank_list:
        row[0] = init_pos
        init_pos += 1

    return list_to_html(sorted_clan_rank_list, col_header)

def get_clan_score(clan_id, req_type='public', score_only=False):
    clan_player_dict    = {}

    if req_type == 'private':
        clan_id_list    = config.clan_id_dict[clan_id]['clan_id']
    elif req_type == 'public':
        clan_id_list    = config.clan_id_single_dict[clan_id]['clan_id']

    player_full_db      = config.player_full_db_file

    if os.path.exists(player_full_db) == False:
        return get_static_page('error.html') 

    with open(player_full_db,'r') as json_file:
        player_data = json.load(json_file)

        init_rank           = 1
        col_header_key      = config.col_header_key()

        # for all the players in the main DB
        for key in player_data:
            if str(player_data[key]['clan_id']) in clan_id_list:

                tmp_dict = {}

                tmp_dict[init_rank] = { \
                        'rank'          :init_rank,
                        'name'          :player_data[key]['name'],
                        'user_id'       :player_data[key]['user_id'],
                        'country_id'    :player_data[key]['country_id'],
                        'clan_tag'      :player_data[key]['clan_tag'],
                        'clan_name'     :player_data[key]['clan_name'],
                        'trophies'      :player_data[key]['trophies'],
                        'leg_trophies'  :player_data[key]['leg_trophies'],
                        'max_trophies'  :player_data[key]['max_trophies'],
                        'game_win'      :player_data[key]['game_win'],
                        'game_total'    :player_data[key]['game_total'],
                        'win_ratio'     :player_data[key]['win_ratio'],
                        'app_version'   :player_data[key]['app_version'],
                        'player_level'  :player_data[key]['player_level']}

                clan_player_dict = {**clan_player_dict, **tmp_dict}

                init_rank += 1

        if req_type == 'public':
            clan_player_dict = dict(islice(clan_player_dict.items(),20))

        total_score = get_clan_score_total(get_clan_score_from_dict(clan_player_dict))

        if score_only is True:
            return total_score

        return dict_to_html(clan_player_dict,total_score)

def get_clan_score_from_dict(clan_player_dict):
    just_clan_score = []

    for key in clan_player_dict:
        just_clan_score.append(clan_player_dict[key]['trophies'])

    return just_clan_score

def get_clan_score_total(clan_player_list):

    ratio_val   = [0.4,0.3,0.2,0.1]
    init_rank   = 0
    group_size  = 5
    total_score = 0

    for i in range(len(ratio_val)):
        sub_group = clan_player_list[init_rank:init_rank+group_size]

        for j in range(len(sub_group)):
            total_score += sub_group[j] * ratio_val[i]

        init_rank += group_size

    return int(total_score)

def get_all_ranks(num_results,country_code,fetch_page_size):

    final_dict  = {}
    num_results = (int)(num_results)
    range_val   = fetch_page_size
    player_db   = config.player_db_file.format(country_code)

    for i in range(num_results):

        l_lim,u_lim = get_rank_range_limits(i, range_val)
        init_rank 	= i*range_val + 1
        resp_dict 	= fetch_rank_details(l_lim,u_lim,init_rank, country_code)
        final_dict 	= {**final_dict, **resp_dict}

    with open(player_db, 'w') as fp:
        json.dump(final_dict, fp)

def get_rank_range_limits(n, range_val):
    lower_limit = 1 + n*(range_val)
    upper_limit = lower_limit + (range_val-1)

    return lower_limit,upper_limit

def get_full_details():
    player_dict = {}

    player_db       = config.player_db_file.format('ALL')
    player_full_db  = config.player_full_db_file
    num_entries     = config.full_detail_num_entries()
    init_val        = 1
    
    while os.path.exists(player_db) == False:
        time.sleep(1)

    with open(player_db,'r') as json_file:
        player_data = json.load(json_file)
        
        for key in player_data:

            if init_val > num_entries:
                break

            device_id   = player_data[key]['device_id']
            tmp_dict    = fetch_player_full_details(device_id,init_val)
            player_dict = {**player_dict, **tmp_dict}
            init_val   += 1

            if sys.argv[1] == '1':
                print('[INFO] Fetched details for rank {}'.format(init_val-1))

    with open(player_full_db, 'w') as fp:
        json.dump(player_dict, fp)

def get_player_clan(each_player):
    clan_tag = ''
    clan_id  = ''
    clan_name= ''
    try:
        clan_tag = each_player['clanTag']
        clan_id  = each_player['clanId']
        clan_name= each_player['clanName']
    except KeyError:
        clan_tag = '----'
        clan_id  = '----'
        clan_name= '----'

    return clan_tag,clan_id,clan_name

def url_fetch_error_handle(url_str):

    response_json = {}

    while True:
        try:
            req_obj = requests.get(url_str)
            response_json = json.loads(req_obj.text)
            break
        except:
            time.sleep(config.error_sleep_duration)
            if sys.argv[1] == '1':
                print('[INFO] Error while fetching/loading')

    return response_json


def fetch_player_full_details(device_id,rank_val):
    url_str = 'http://api.skidstorm.cmcm.com/v2/profile/{}'.format(device_id)

    q = url_fetch_error_handle(url_str)

    resp_dict = {}

    row = q['profile']

    country_db  = config.country_db()
    country_id  = country_db[row['country']].upper()

    clan_tag, clan_id, clan_name = get_player_clan(row)

    game_win    = int(row['wins'])
    game_total  = int(row['gamesPlayed'])
    win_ratio   = "%.2f" % round(float(game_win*100/game_total),2)
    time_played = second_to_days_hours(int(row['profile']['timePlayed']))
    time_played = '{0:02.0f} Days {1:02.0f} Hours {2:02.0f} Mins'.format(*time_played)

    acc_created = row['created'].split(' ')[0]
    last_login  = row['last_login'].split(' ')[0]
    
    resp_dict[rank_val] = {
            'rank'          :rank_val,
            'name'          :row['username'],
            'user_id'       :row['id'],
            'country_id'    :country_id,
            'clan_tag'      :clan_tag,
            'clan_id'       :clan_id,
            'clan_name'     :clan_name,
            'trophies'      :row['rank'],
            'leg_trophies'  :row['legendaryTrophies'],
            'max_trophies'  :row['economy']['maxRank'],
            'game_win'      :row['wins'],
            'game_total'    :row['gamesPlayed'],
            'win_ratio'     :str(win_ratio),
            'time_played'   :str(time_played),
            'num_purchase'  :str(len(row['economy']['purchases'])),
            'diamonds'      :row['economy']['diamonds'],
            'coins'         :row['economy']['coins'],
            'gasoline'      :row['economy']['gasolineBucket'],
            'vip_level'     :row['economy']['vipInfo']['vipMaxLevel'],
            'vip_exp'       :row['economy']['vipInfo']['vipExp'],
            'player_level'  :row['economy']['xp']['level'],
            'app_version'   :row['version'],
            'acc_created'   :str(acc_created),
            'last_login'    :str(last_login),
            'one_signal'    :row['onesignal'],
            'device_id'     :row['device']}

    return resp_dict

def fetch_rank_details(num_1, num_2, rank_val, country_code):

    url_str = 'http://api.skidstorm.cmcm.com/v2/rank/list/{0}-{1}/{2}'.format(num_1,num_2,country_code)

    q = url_fetch_error_handle(url_str)

    resp_dict = {}

    for each_player in q['ranks']:

        resp_dict[rank_val] = {
                'name'          :each_player['username'],
                'trophies'      :each_player['rank'],
                'device_id'     :each_player['device'],
                'clan_tag'      :each_player['clanTag'],
                'clan_name'     :each_player['clanName'],
                'clan_id'       :each_player['clanId'],
                'leg_trophies'  :each_player['legendaryTrophies']}

        resp_dict[rank_val] = check_clan_id(resp_dict[rank_val])

        rank_val += 1

    return resp_dict

def check_clan_id(player_data):
    if player_data['clan_tag'] is None or \
        player_data['clan_id'] is None or \
        player_data['clan_name'] is None:

        player_data['clan_tag']     = '----'
        player_data['clan_id']      = '0'
        player_data['clan_name']    = '----'

    return player_data

def open_player_full_db(ret_type='html',req_type='public'):
    
    player_full_db = config.player_full_db_file
    
    if os.path.exists(player_full_db) == False:
        return get_static_page('error.html') 
        
    with open(player_full_db,'r') as json_file:
        player_full_data = json.load(json_file)
    
    if ret_type == 'html':
        return dict_to_html(player_full_data,0,req_type)
    elif ret_type == 'json':
        return player_full_data
    
def open_player_db(country_code,ret_type='html'):
    player_list     = []
    player_db       = config.player_db_file.format(country_code)
    col_header_id   = ['rank', 'name', 'trophies', 'leg_trophies', 'clan_tag']

    if os.path.exists(player_db) == False:
        return get_static_page('error.html') 

    with open(player_db,'r') as json_file:
        player_data = json.load(json_file)

        for key in player_data:
            player_list.append([
                key,
                player_data[key]['name'],
                player_data[key]['trophies'],
                player_data[key]['leg_trophies'],
                player_data[key]['clan_tag']])

        if ret_type == 'html':
            return list_to_html(player_list,col_header_id)
        elif ret_type == 'json':
            return player_data

def list_to_html(player_list, col_header_id):
    col_header          = config.col_header
    style_string        = config_html.style_string
    responsive_string   = config_html.responsive_string
    table_preamble      = config_html.table_preamble
    bgcolor_database    = config_html.bgcolor_database

    big_string = \
    '''<html>{}{}<body bgcolor="{}">'''.format(responsive_string,style_string,bgcolor_database)

    if len(col_header_id) is 4:
        big_string += config_html.list_to_html_clan_rank_header
    elif len(col_header_id) is 5:
        big_string += config_html.list_to_html_country_header

    big_string += table_preamble

    # creating table header
    table_string = '<tr>'
    for i in col_header_id:
        table_string += '''<td class="table-heading" nowrap>{}</td>'''.format(col_header[i][1])
    table_string += '</tr>'

    # adding table header to main html
    big_string += table_string

    # creating player table
    for row in player_list:

        # creating row for a single player
        table_row = '<tr>'
        for i in range(len(col_header_id)):

            table_row += '''<td class={}>{}</td>'''.format( \
                col_header[col_header_id[i]][0], row[i])

        table_row += '</tr>'
 
        # adding row to main html
        big_string += table_row

    big_string += '</table></body></html>'

    return big_string

def second_to_days_hours(time_second):
    sec_day     = 86400
    sec_hour    = 3600
    sec_min     = 60

    num_days    = time_second // sec_day
    sec_rem     = time_second - (num_days * sec_day)

    num_hours   = sec_rem // sec_hour
    sec_rem     = sec_rem - (num_hours * sec_hour)

    num_mins    = sec_rem // sec_min

    return [num_days, num_hours, num_mins]

def get_static_page(page_name='index.html'):
    return bottle.static_file(page_name, root='./public')

def fetch_data_infinite(num_results_world,num_results_country,fetch_interval,country_list):

    size_per_fetch = config.size_per_fetch

    while True:
        if sys.argv[1] == '1':
            print('[INFO] Fetching for country ALL')

        store_datetime(datetime.datetime.now(),'before_ALL')

        get_all_ranks(num_results_world,'ALL',size_per_fetch)

        store_datetime(datetime.datetime.now(),'after_ALL')
        
        store_datetime(datetime.datetime.now(),'before_country')
    
        for country in country_list:
            if sys.argv[1] == '1':
                print('[INFO] Fetching for country {}'.format(country))
    
            get_all_ranks(num_results_country,country,size_per_fetch)
        
        store_datetime(datetime.datetime.now(),'after_country')

        store_datetime(datetime.datetime.now(),'before_full')

        get_full_details()

        store_datetime(datetime.datetime.now(),'after_full')

        if sys.argv[1] == '1':
            print('[INFO] Going to sleep for {} seconds'.format(fetch_interval))

        time.sleep(fetch_interval)

def open_time_data():
    date_json = config.date_json_filename

    date_obj = datetime.datetime.now()
    current_time_str = date_obj.strftime("%-I:%M:%S %p, %d %b %Y") 

    with open(date_json,'r') as fp:
        date_dict = json.loads(fp.read())

        tmp_string = config_html.date_file_string

        webpage_string = tmp_string.format( \
                config_html.responsive_string,
                config_html.style_string,
                config_html.bgcolor_body,
                current_time_str,
                date_dict['server_started'],
                date_dict['before_ALL'],
                date_dict['after_ALL'],
                date_dict['before_country'],
                date_dict['after_country'],
                date_dict['before_full'],
                date_dict['after_full'],
                config_html.page_ending)

        return webpage_string

def store_datetime(date_obj,date_id):
    date_json = config.date_json_filename
    date_dict = {}

    with open(date_json,'r') as fp:
        date_dict = json.loads(fp.read())
        date_dict[date_id] = date_obj.strftime("%-I:%M:%S %p, %d %b %Y")

    json.dump(date_dict, open(date_json,'w'))

def create_data_dir():
    if os.path.exists(config.player_db_file_dir) == False:
        os.mkdir(config.player_db_file_dir)

def create_empty_json():
    date_json = config.date_json_filename

    if os.path.exists(date_json) == False:

        empty_db = config.empty_db

        with open(date_json,'w') as fp:
            json.dump(empty_db,fp)

def get_season_end():
    date_end_dict = config.season_end

    date_end = datetime.date( \
            date_end_dict['yyyy'], \
            date_end_dict['mm'], \
            date_end_dict['dd'])

    date_start = datetime.date.today()

    diff_day = date_end - date_start

    return season_end_page(str(diff_day))

def season_end_page(diff_day):

    date_end_dict       = config.season_end
    date_end_str        = '{} / {} / {}'.format(date_end_dict['dd'],date_end_dict['mm'],date_end_dict['yyyy'])
    diff_day            = (diff_day[0:2]).strip()

    style_string        = config_html.style_string
    responsive_string   = config_html.responsive_string
    bgcolor_body        = config_html.bgcolor_body
    page_ending         = config_html.page_ending

    season_end_string   = config_html.season_end_string.format(responsive_string,style_string, \
    bgcolor_body,diff_day,date_end_str,page_ending)

    return season_end_string 

def open_img_clan_score():
    return config_html.possible_clan_score

def do_clan_score():
    player_full_db = config.player_full_db_file

    if os.path.exists(player_full_db) == False:
        return get_static_page('error.html') 

    clan_player_dict = {}
    player_id_list = bottle.request.forms.get('player_id_list')
    player_id_list = player_id_list.split('\n')
    player_id_list = list(filter(None,player_id_list))
    player_id_list = list(map(int,player_id_list))

    with open(player_full_db,'r') as json_file:
        player_data = json.load(json_file)

        init_rank      = 1
        tmp_dict       = {}
        col_header_key = config.col_header_key()

        # for every ID in the user given list
        for user_id_val in player_id_list:

            # for all the players in the main DB
            for key in player_data:

                # if the player ID matches the current player ID
                if player_data[key]['user_id'] == user_id_val:
                    tmp_dict[init_rank] = { \
                            'rank'          :player_data[key]['rank'],
                            'name'          :player_data[key]['name'],
                            'user_id'       :player_data[key]['user_id'],
                            'country_id'    :player_data[key]['country_id'],
                            'clan_tag'      :player_data[key]['clan_tag'],
                            'clan_name'     :player_data[key]['clan_name'],
                            'trophies'      :player_data[key]['trophies'],
                            'leg_trophies'  :player_data[key]['leg_trophies'],
                            'max_trophies'  :player_data[key]['max_trophies'],
                            'game_win'      :player_data[key]['game_win'],
                            'game_total'    :player_data[key]['game_total'],
                            'win_ratio'     :player_data[key]['win_ratio'],
                            'app_version'   :player_data[key]['app_version'],
                            'player_level'  :player_data[key]['player_level']}

                    clan_player_dict = {**clan_player_dict, **tmp_dict}
                    init_rank += 1
                    break

        total_score = get_clan_score_total(get_clan_score_from_dict(clan_player_dict))

        return dict_to_html(clan_player_dict,total_score)
    
def dict_to_html(player_dict, clan_score=0, req_type='public'):

    responsive_string   = config_html.responsive_string
    style_string        = config_html.style_string
    table_preamble      = config_html.table_preamble
    bgcolor_database    = config_html.bgcolor_database
    col_header_list     = [] 

    big_string = '<html>{}{}<body bgcolor=\"{}\">'.format(responsive_string,style_string,bgcolor_database)

    if clan_score != 0:
        score_html = \
        '''
        <div class="header">
            <br>
            <h1>Clan : {}</h1>
            <h2>Total Score : {}</h1>
            <br>
        </div><br>
        '''.format(player_dict[1]['clan_name'],clan_score)
        big_string += score_html

    big_string += table_preamble

    col_header_key  = config.col_header_key(req_type)
    col_header      = config.col_header

    # creating table header
    table_string = '<tr>'
    for i in col_header_key:
        table_string += "<td class=\"table-heading\" nowrap>{}</td>".format(col_header[i][1])
    table_string += '</tr>'

    # adding table header to main string
    big_string += table_string

    for key in player_dict:

        # creating single row for a player
        table_row = '<tr>'

        for i in col_header_key:
            table_row += '<td class={}>{}</td>'.format(col_header[i][0], player_dict[key][i])

        table_row += '</tr>'

        # adding player row to main string
        big_string += table_row

    big_string += '</table></body></html>'

    return big_string

def main():

    num_pages_fetch_world   = config.num_pages_fetch_world
    num_pages_fetch_country = config.num_pages_fetch_country
    fetch_interval          = config.fetch_interval()
    country_list            = config.country_list()

    create_data_dir()
    create_empty_json()
    store_datetime(datetime.datetime.now(),'server_started')

    thread_player_db = threading.Thread(target=fetch_data_infinite, \
            args=(num_pages_fetch_world,num_pages_fetch_country, \
            fetch_interval, country_list,))
    thread_player_db.start()

    bottle.route('/',                                               method='GET')(get_static_page)
    bottle.route('/<page_name>',                                    method='GET')(get_static_page)

    bottle.route('/gen/show_rank/<country_code>/<ret_type>',        method='GET')(open_player_db)
    bottle.route('/gen/show_rank/<country_code>',                   method='GET')(open_player_db)
    bottle.route('/gen/get_season_end',                             method='GET')(get_season_end)
    bottle.route('/gen/get_full_details',                           method='GET')(open_player_full_db)
    bottle.route('/gen/get_clan_score/<clan_id>',                   method='GET')(get_clan_score)
    bottle.route('/gen/get_clan_rank',                              method='GET')(get_clan_rank)
    bottle.route('/gen/get_time_data',                              method='GET')(open_time_data)

    bottle.route('/secret/get_clan_score/<clan_id>/<req_type>',     method='GET')(get_clan_score)
    bottle.route('/secret/get_full_details/<ret_type>',             method='GET')(open_player_full_db)
    bottle.route('/secret/get_full_details/<ret_type>/<req_type>',  method='GET')(open_player_full_db)
    bottle.route('/secret/img_clan_score',                          method='GET')(open_img_clan_score)
    bottle.route('/secret/do_clan_score',                           method='POST')(do_clan_score)

    server_type = 'wsgiref'
    if config.is_heroku_env() == False:
        server_type = 'paste'

    bottle.run(host = '0.0.0.0', server = server_type, port = int(os.environ.get('PORT', 5000)), debug = False)

if __name__ == '__main__':
    main()
