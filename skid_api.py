#!/usr/bin/env python3

import json
import requests
import threading
import time
import os
import bottle

player_db_file  = 'data/player_db_{}.json'
fetch_interval  = 120

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
                'leg_trophies'  :each_player['legendaryTrophies']
                }

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

    col_header = ['Sl. No.', 'Name', 'Trophies', 'Legendary Trophies', 'Clan Tag']

    big_string = '<html><body><table>'
    big_string += \
            "<tr> \
                <td>{}</td> \
                <td>{}</td> \
                <td>{}</td> \
                <td>{}</td> \
                <td>{}</td> \
            </tr>".format(*col_header)

    for row in player_list:
        big_string += \
            "<tr> \
                <td>{}</td> \
                <td>{}</td> \
                <td>{}</td> \
                <td>{}</td> \
                <td>{}</td> \
            </tr>".format(row[0],row[1],row[2],row[3],row[4])

    big_string += '</table></body></html>'

    return big_string

def get_default_page():
    return bottle.static_file('index.html', root='./public')

def fetch_data_infinite(num_results,alt_num_results):
    while True:
        get_all_ranks(num_results,'ALL')
        get_all_ranks(alt_num_results,'in',100)
        get_all_ranks(alt_num_results,'it',100)
        get_all_ranks(alt_num_results,'nl',100)
        get_all_ranks(alt_num_results,'fr',100)
        get_all_ranks(alt_num_results,'us',100)
        get_all_ranks(alt_num_results,'be',100)
        get_all_ranks(alt_num_results,'es',100)

        time.sleep(fetch_interval)

def main():
    thread_1 = threading.Thread(target=fetch_data_infinite, args=(10,1,))
    thread_1.start()

    bottle.route('/', method='GET')(get_default_page)
    bottle.route('/api/get_rank/<num_results>', method='GET')(get_all_ranks)
    bottle.route('/gen/show_rank/<country_code>', method='GET')(open_player_db)

    bottle.run(host = '0.0.0.0', port = int(os.environ.get('PORT', 5000)), debug = False)

if __name__ == '__main__':
    main()
