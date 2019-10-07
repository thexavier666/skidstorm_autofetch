#!/usr/bin/env python3

import json
import requests
import threading
import time
import os
import bottle

player_db_file_dir  = 'data/'
player_db_file      = player_db_file_dir + 'player_db_{}.json'

clan_id_dict = {
        'revo' : ['93633','123276','119234','126321'],
        'cyre' : ['138751'],
        'espa' : ['150634'],
        'noss' : ['188811'],
        'sx'   : ['163287'],
        'free' : ['0']}

def get_clan_score(clan_id):
    clan_player_list    = []
    country_code        = 'ALL'
    clan_id_list        = clan_id_dict[clan_id]
    init_rank           = 1

    while os.path.exists(player_db_file.format(country_code)) == False:
        time.sleep(1)

    with open(player_db_file.format(country_code),'r') as json_file:
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

    ratio_val = [0.4,0.3,0.2,0.1]

    init_rank = 0
    group_size = 5
    total_score = 0

    for i in range(len(ratio_val)):
        sub_group = clan_player_list[init_rank:init_rank+5]

        for j in range(len(sub_group)):
            total_score += sub_group[j][2] * ratio_val[i]

        init_rank += group_size

    return int(total_score)

def get_all_ranks(num_results,country_code,fetch_page_size=100):

    final_dict = {}

    num_results = (int)(num_results)

    range_val = fetch_page_size

    for i in range(num_results):

        l_lim,u_lim = get_rank_range_limits(i, range_val)

        init_rank = i*range_val + 1

        resp_dict = get_rank_range_details(l_lim,u_lim,init_rank, country_code)

        final_dict = {**final_dict, **resp_dict}

    with open(player_db_file.format(country_code), 'w') as fp:
        json.dump(final_dict, fp)

    return final_dict

def get_rank_range_limits(n, range_val):
    lower_limit = 1 + n*(range_val)
    upper_limit = lower_limit + (range_val-1)

    return lower_limit,upper_limit

def get_rank_range_details(num_1, num_2, rank_val, country_code):

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
        player_data['clan_tag']     = 'FREE_AGENT'
        player_data['clan_name']    = 'FREE_AGENT'

    return player_data

def open_player_db(country_code):
    player_list = []

    while os.path.exists(player_db_file.format(country_code)) == False:
        time.sleep(1)

    with open(player_db_file.format(country_code),'r') as json_file:
        player_data = json.load(json_file)

        for key in player_data:
            player_list.append([
                key,
                player_data[key]['name'],
                player_data[key]['trophies'],
                player_data[key]['leg_trophies'],
                player_data[key]['clan_tag']])

    return list_to_html(player_list)

def list_to_html(player_list, total_score = 0):

    col_header = ['Sl. No.', 'Name', 'Trophies', 'Legendary Trophies', 'Clan']

    responsive_string = "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"

    style_string = \
    "<head> \
        <link href=\"https://fonts.googleapis.com/css?family=Roboto+Mono&display=swap\" rel=\"stylesheet\"> \
        <style> \
            body{ \
                font-family: 'Roboto Mono', monospace; \
                font-size: 12px; \
            } \
            table{ \
                border:1px solid black; \
                margin-left:auto; \
                margin-right:auto; \
            } \
            td.num_type{ \
                text-align: right; \
            } \
        </style> \
    </head>"

    big_string = '<html>{}{}<body bgcolor=\"#66d48f\">'.format(responsive_string,style_string)

    if total_score != 0:
        score_string = '<center><h1>Clan Score - {}</h1></center>'.format(total_score)
        big_string += score_string

    table_preamble = '<table cellpadding=\"5\">'

    big_string += table_preamble

    big_string += \
            "<tr> \
                <td><b>{}</b></td> \
                <td><b>{}</b></td> \
                <td><b>{}</b></td> \
                <td><b>{}</b></td> \
                <td><b>{}</b></td> \
            </tr>".format(*col_header)

    for row in player_list:
        big_string += \
            "<tr> \
                <td class=\"num_type\">{}</td> \
                <td>{}</td> \
                <td class=\"num_type\">{}</td> \
                <td class=\"num_type\">{}</td> \
                <td>{}</td> \
            </tr>".format(row[0],row[1],row[2],row[3],row[4])

    big_string += '</table></body></html>'

    return big_string

def get_static_page(page_name):
    return bottle.static_file(page_name, root='./public')

def get_default_page():
    return bottle.static_file('index.html', root='./public')

def fetch_data_infinite(num_results_world,num_results_country,fetch_interval, country_list):

    size_per_fetch = 100

    while True:
        get_all_ranks(num_results_world,'ALL',size_per_fetch)

        for country in country_list:
            get_all_ranks(num_results_country,country,size_per_fetch)

        time.sleep(fetch_interval)

def create_data_dir():
    if os.path.exists(player_db_file_dir) == False:
        os.mkdir(player_db_file_dir)

def main():

    num_pages_fetch_world = 11
    num_pages_fetch_country = 1
    fetch_interval = 120
    country_list = ['pt','de','pl','cn','in','it','nl','fr','us','be','es','gb']

    thread_1 = threading.Thread(target=fetch_data_infinite, \
            args=(num_pages_fetch_world,num_pages_fetch_country, \
            fetch_interval, country_list,))
    thread_1.start()

    create_data_dir()

    bottle.route('/',                                           method='GET')(get_default_page)
    bottle.route('/<page_name>',                                method='GET')(get_static_page)
    bottle.route('/api/get_rank/<num_results>/<country_code>',  method='GET')(get_all_ranks)
    bottle.route('/gen/show_rank/<country_code>',               method='GET')(open_player_db)
    bottle.route('/secret/get_clan_score/<clan_id>',            method='GET')(get_clan_score)

    bottle.run(host = '0.0.0.0', port = int(os.environ.get('PORT', 5000)), debug = False)

if __name__ == '__main__':
    main()
