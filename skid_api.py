#!/usr/bin/env python3

import json
import requests
import threading
import time
import os
import bottle
import datetime
import sys

from config_dir import config
from config_dir import config_html

country_list = json.load(open(config.country_list_db,'r'))
country_list = {v: k for k, v in country_list.items()}

def get_clan_score(clan_id):
    clan_player_list    = []
    country_code        = 'ALL'
    clan_id_list        = config.clan_id_dict[clan_id]
    init_rank           = 1
    player_db           = config.player_db_file.format(country_code)

    while os.path.exists(player_db) == False:
        time.sleep(1)

    with open(player_db,'r') as json_file:
        player_data = json.load(json_file)

        for key in player_data:
            if player_data[key]['clan_id'] in clan_id_list:

                tmp = [ init_rank, \
                        player_data[key]['name'], \
                        player_data[key]['trophies'], \
                        player_data[key]['leg_trophies'], \
                        player_data[key]['clan_name']]

                clan_player_list.append(tmp)

                init_rank += 1

        total_score = get_clan_score_total(clan_player_list)

        return list_to_html(clan_player_list,total_score)

def get_clan_score_total(clan_player_list):

    ratio_val   = [0.4,0.3,0.2,0.1]
    init_rank   = 0
    group_size  = 5
    total_score = 0

    for i in range(len(ratio_val)):
        sub_group = clan_player_list[init_rank:init_rank+5]

        for j in range(len(sub_group)):
            total_score += sub_group[j][2] * ratio_val[i]

        init_rank += group_size

    return int(total_score)

def get_all_ranks(num_results,country_code,fetch_page_size):

    final_dict  = {}
    num_results = (int)(num_results)
    range_val   = fetch_page_size
    player_db   = config.player_db_file.format(country_code)

    for i in range(num_results):

        l_lim,u_lim = get_rank_range_limits(i, range_val)

        init_rank = i*range_val + 1

        resp_dict = fetch_rank_details(l_lim,u_lim,init_rank, country_code)

        final_dict = {**final_dict, **resp_dict}

    with open(player_db, 'w') as fp:
        json.dump(final_dict, fp)

    return final_dict

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
                print('[FULL_DB] Fetched details for {}'.format(device_id))

    with open(player_full_db, 'w') as fp:
        json.dump(player_dict, fp)

    return player_dict

def get_player_clan(each_player):
    if each_player['profile']['clan'] == '{}':
        return '--'
    else:
        return each_player['profile']['clan']['tag']

def fetch_player_full_details(device_id,rank_val):
    url_str = 'http://api.skidstorm.cmcm.com/v2/profile/{}'.format(device_id)

    p = requests.get(url_str)
    q = json.loads(p.text)

    resp_dict = {}

    row = q['profile']

    game_win    = int(row['wins'])
    game_total  = int(row['gamesPlayed'])
    win_ratio   = "%.2f" % round(float(game_win*100/game_total),2)
    acc_created = row['created'].split(' ')[0]
    last_login  = row['last_login'].split(' ')[0]
    clan_tag    = get_player_clan(row)
    country_id = country_list[row['country']].upper()
    
    resp_dict[rank_val] = {
            'name'          :row['username'],
            'user_id'       :row['id'],
            'country_id'    :country_id,
            'clan_tag'      :clan_tag,

            'trophies'      :row['rank'],
            'leg_trophies'  :row['legendaryTrophies'],
            'max_trophies'  :row['economy']['maxRank'],

            'game_win'      :row['wins'],
            'game_total'    :row['gamesPlayed'],
            'win_ratio'     :str(win_ratio),

            'diamonds'      :row['economy']['diamonds'],
            'coins'         :row['economy']['coins'],
            'gasoline'      :row['economy']['gasolineBucket'],
            'vip_level'     :row['economy']['vipInfo']['vipExp'],
            'vip_exp'       :row['economy']['vipInfo']['vipMaxLevel'],
            'player_level'  :row['economy']['xp']['level'],

            'app_version'   :row['version'],
            'acc_created'   :str(acc_created),
            'last_login'    :str(last_login),
            'one_signal'    :row['onesignal'],
            'device_id'     :row['device']}

    return resp_dict

def fetch_rank_details(num_1, num_2, rank_val, country_code):

    url_str = 'http://api.skidstorm.cmcm.com/v2/rank/list/{0}-{1}/{2}'.format(num_1,num_2,country_code)

    p = requests.get(url_str)
    q = json.loads(p.text)

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

        player_data['clan_id']      = '0'
        player_data['clan_tag']     = '--'
        player_data['clan_name']    = '--'

    return player_data

def open_player_full_db(ret_type='html'):
    
    player_full_db = config.player_full_db_file
    
    while os.path.exists(player_full_db) == False:
        time.sleep(1)
        
    with open(player_full_db,'r') as json_file:
        player_full_data = json.load(json_file)
    
    if ret_type == 'html':
        return dict_to_html(player_full_data)
    elif ret_type == 'json':
        return player_full_data
    
def open_player_db(country_code,ret_type='html'):
    player_list = []
    player_db   = config.player_db_file.format(country_code)

    while os.path.exists(player_db) == False:
        time.sleep(1)

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
            return list_to_html(player_list)
        elif ret_type == 'json':
            return player_data

def list_to_html(player_list, total_score = 0):

    col_header = ['Sl. No.', 'Name', 'Trophies', 'Legendary Trophies', 'Clan']

    style_string        = config_html.style_string
    responsive_string   = config_html.responsive_string
    table_preamble      = config_html.table_preamble
    bgcolor_clan        = config_html.bgcolor_clan

    big_string = '<html>{}{}<body bgcolor=\"{}\">'.format(responsive_string,style_string % (12),bgcolor_clan)

    if total_score != 0:
        score_string = '<center><h1>Clan Score - {}</h1></center>'.format(total_score)
        big_string += score_string

    big_string += table_preamble

    big_string += \
            "<tr> \
                <td><b>{}</b></td> \
                <td><b>{}</b></td> \
                <td><b>{}</b></td> \
                <td><b>{}</b></td> \
                <td align=\"center\"><b>{}</b></td> \
            </tr>".format(*col_header)

    for row in player_list:
        big_string += \
            "<tr> \
                <td class=\"num_type\">{}</td> \
                <td>{}</td> \
                <td class=\"num_type\">{}</td> \
                <td class=\"num_type\">{}</td> \
                <td align=\"center\">{}</td> \
            </tr>".format(row[0],row[1],row[2],row[3],row[4])

    big_string += '</table></body></html>'

    return big_string

def get_static_page(page_name='index.html'):
    return bottle.static_file(page_name, root='./public')

def fetch_data_infinite(num_results_world,num_results_country,fetch_interval, country_list):

    size_per_fetch = config.size_per_fetch

    while True:
        if sys.argv[1] == '1':
            print('[HALF_DB] Fetching for country ALL')

        get_all_ranks(num_results_world,'ALL',size_per_fetch)

        for country in country_list:
            if sys.argv[1] == '1':
                print('[HALF_DB] Fetching for country {}'.format(country))

            get_all_ranks(num_results_country,country,size_per_fetch)
        
        get_full_details()

        if sys.argv[1] == '1':
            print('[INFO] Going to sleep for {} seconds'.format(fetch_interval))

        time.sleep(fetch_interval)

def create_data_dir():
    if os.path.exists(config.player_db_file_dir) == False:
        os.mkdir(config.player_db_file_dir)

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

    date_end_dict = config.season_end
    date_end_str = '{} / {} / {}'.format(date_end_dict['dd'],date_end_dict['mm'],date_end_dict['yyyy'])

    diff_day = (diff_day[0:2]).strip()

    style_string = config_html.style_string
    bgcolor_season_end = config_html.bgcolor_season_end

    big_string = \
    "<html>{}<body bgcolor=\"{}\"><center> \
        <br><br>Season ends in<br><br><b>{} days</b><br><br> \
        which is on<br><br><b>{} GMT</b> \
    <center></body></html>".format(style_string % (36),bgcolor_season_end,diff_day,date_end_str)

    return big_string
    
def dict_to_html(player_dict):
    col_header = ['Sl. No.','Username','Player ID','Country','Clan Tag', \
            'Trophies','Legendary Trophies','Max Trophies', \
            'Wins','Games Played','Win Ratio',
            'Diamonds','Coins','Gasoline Buckets','VIP Level','VIP Experience','Level', \
            'App Version','A/C Created','Last Login','One Signal','Device ID',]

    responsive_string   = config_html.responsive_string
    style_string        = config_html.style_string
    table_preamble      = config_html.table_preamble
    bgcolor_database    = config_html.bgcolor_database

    big_string = '<html>{}{}<body bgcolor=\"{}\">'.format(responsive_string,style_string % (12),bgcolor_database)

    big_string += table_preamble

    big_string += \
            "<tr> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
                <td align=\"center\" nowrap><b>{}</b></td> \
            </tr>".format(*col_header)

    for key in player_dict:
        tmp_list = list(player_dict[key].values())
        big_string += \
            "<tr> \
                <td class=\"num_type\">{}</td> \
                <td nowrap>{}</td> \
                <td class=\"num_type\">{}</td> \
                <td align=\"center\">{}</td> \
                <td align=\"center\">{}</td> \
                <td class=\"num_type\">{}</td> \
                <td class=\"num_type\">{}</td> \
                <td class=\"num_type\">{}</td> \
                <td class=\"num_type\">{}</td> \
                <td class=\"num_type\">{}</td> \
                <td class=\"num_type\">{}</td> \
                <td class=\"num_type\">{}</td> \
                <td class=\"num_type\">{}</td> \
                <td class=\"num_type\">{}</td> \
                <td class=\"num_type\">{}</td> \
                <td class=\"num_type\">{}</td> \
                <td class=\"num_type\">{}</td> \
                <td>{}</td> \
                <td nowrap>{}</td> \
                <td nowrap>{}</td> \
                <td nowrap>{}</td> \
                <td>{}</td> \
            </tr>".format(key,*tmp_list)

    big_string += '</table></body></html>'

    return big_string

'''
# this code is disabled 
# because running 2 threads are disabled in heroku

def fetch_full_data_infinite(fetch_interval):

    while True:
        get_full_details()
        print("FULL DATA FETCTCHED")
        time.sleep(fetch_interval)
'''

def main():

    num_pages_fetch_world   = config.num_pages_fetch_world
    num_pages_fetch_country = config.num_pages_fetch_country
    fetch_interval          = config.fetch_interval()
    fetch_interval_big_db   = config.fetch_interval_big_db
    country_list            = config.country_list

    thread_player_db = threading.Thread(target=fetch_data_infinite, \
            args=(num_pages_fetch_world,num_pages_fetch_country, \
            fetch_interval, country_list,))
    thread_player_db.start()

    '''
    thread_detail_db = threading.Thread(target=fetch_full_data_infinite, \
            args=(fetch_interval_big_db,))
    thread_detail_db.start()
    '''

    create_data_dir()

    bottle.route('/',                                           method='GET')(get_static_page)
    bottle.route('/<page_name>',                                method='GET')(get_static_page)
    bottle.route('/api/get_rank/<num_results>/<country_code>',  method='GET')(get_all_ranks)

    bottle.route('/gen/show_rank/<country_code>/<ret_type>',    method='GET')(open_player_db)
    bottle.route('/gen/show_rank/<country_code>',               method='GET')(open_player_db)
    bottle.route('/gen/get_season_end',                         method='GET')(get_season_end)

    bottle.route('/secret/get_clan_score/<clan_id>',            method='GET')(get_clan_score)
    bottle.route('/secret/get_full_details/<ret_type>',         method='GET')(open_player_full_db)
    bottle.route('/secret/get_full_details',                    method='GET')(open_player_full_db)

    bottle.run(host = '0.0.0.0', port = int(os.environ.get('PORT', 5000)), debug = False)

if __name__ == '__main__':
    main()
