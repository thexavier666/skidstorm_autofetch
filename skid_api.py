#!/usr/bin/env python3

import json
import requests
import threading
import time
import os
import bottle

player_db_file_dir  = 'data/'
player_db_file      = player_db_file_dir + 'player_db_{}.json'
fetch_interval      = 120

clan_id_dict = {
        'revo' : ['93633','123276','119234','126321'],
        'cyre' : ['138751'],
        'espa' : ['150634'],
        'noss' : ['188811'],
        'free' : ['None']}

def get_clan_score_wrapper(clan_id):
    return get_clan_score(clan_id_dict[clan_id])

def get_clan_score(clan_id_list):
    clan_player_list    = []
    init_rank           = 1
    country_code        = 'ALL'

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

        return list_to_html(clan_player_list)

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

        rank_val += 1

    return resp_dict

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

def list_to_html(player_list):

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

    big_string = '<html>{}{}<body bgcolor=\"#66d48f\"><table cellpadding=\"5\">'.format(responsive_string,style_string)
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

def get_static_page(page_name='index.hmtl'):
    return bottle.static_file(page_name, root='./public')

def get_default_page():
    return bottle.static_file('index.html', root='./public')

def fetch_data_infinite(num_results,alt_num_results):

    country_list = ['in','it','nl','fr','us','be','es','gb']

    while True:
        get_all_ranks(num_results,'ALL',100)

        for country in country_list:
            get_all_ranks(alt_num_results,country,100)

        time.sleep(fetch_interval)

def create_data_dir():
    if os.path.exists(player_db_file_dir) == False:
        os.mkdir(player_db_file_dir)

def main():
    thread_1 = threading.Thread(target=fetch_data_infinite, args=(10,1,))
    thread_1.start()

    create_data_dir()

    bottle.route('/', method='GET')(get_default_page)
    bottle.route('/<page_name>', method='GET')(get_static_page)
    bottle.route('/api/get_rank/<num_results>/<country_code>', method='GET')(get_all_ranks)
    bottle.route('/gen/show_rank/<country_code>', method='GET')(open_player_db)
    bottle.route('/secret/get_clan_score/<clan_id>', method='GET')(get_clan_score_wrapper)

    bottle.run(host = '0.0.0.0', port = int(os.environ.get('PORT', 5000)), debug = False)

if __name__ == '__main__':
    main()
