#!/usr/bin/env python3

import json
import requests
import threading
import time

from flask import Flask
app = Flask(__name__)

player_db_file  = 'player_db.json'
fetch_page_size = 100
fetch_interval  = 60

def get_rank_range_details(num_1, num_2, rank_val):

    url_str = 'http://api.skidstorm.cmcm.com/v2/rank/list/{0}-{1}/ALL'.format(num_1,num_2)

    p = requests.get(url_str)
    q = json.loads(p.text)

    resp_dict = {}

    for each_player in q['ranks']:

        resp_dict[rank_val] = {
                'name'      :each_player['username'],
                'trophies'  :each_player['rank'], 
                'device_id' :each_player['device'], 
                'clan_tag'  :each_player['clanTag'],
                'clan_name' :each_player['clanName']}

        rank_val += 1

    return resp_dict

def get_rank_range_limits(n, range_val):
    lower_limit = 1 + n*(range_val)
    upper_limit = lower_limit + (range_val-1)

    return lower_limit,upper_limit

@app.route('/api/get_rank/<num_results>')
def get_all_ranks(num_results):

    final_dict = {}

    num_results = (int)(num_results)

    range_val = fetch_page_size

    for i in range(num_results):

        l_lim,u_lim = get_rank_range_limits(i, range_val)

        init_rank = i*range_val + 1

        resp_dict = get_rank_range_details(l_lim,u_lim,init_rank)

        final_dict = {**final_dict, **resp_dict}

    with open(player_db_file, 'w') as fp:
        json.dump(final_dict, fp)

    return final_dict

@app.route('/gen/show_rank')
def open_player_db():
    player_list = []

    with open(player_db_file,'r') as json_file:
        player_data = json.load(json_file)

        for key in player_data:
            player_list.append([
                key,
                player_data[key]['name'],
                player_data[key]['trophies'],
                player_data[key]['clan_tag']])

    return list_to_string(player_list)

def list_to_string(player_list):

    big_string = '<html><body><table>'

    for row in player_list:
        big_string += \
            "<tr> \
                <td>{}</td> \
                <td>{}</td> \
                <td>{}</td> \
                <td>{}</td> \
            </tr>".format(row[0],row[1],row[2],row[3])

    big_string += '</table></body></html>'

    return big_string

@app.route('/')
def get_default_page():
    return "This service is brought to you by xavier666"

def fetch_data_infinite(num_results):
    while True:
        #print("Data fetched at {}".format(time.time()))
        get_all_ranks(num_results)
        time.sleep(fetch_interval)

def main():
    thread_1 = threading.Thread(target=fetch_data_infinite, args=(5,))
    thread_1.start()

    app.run(debug = True)

if __name__ == '__main__':
    main()
