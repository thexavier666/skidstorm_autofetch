# directory in which the fetched data is to be stored
player_db_file_dir  = 'data/'

# name of the json file where the data is to be stored
player_db_file      = player_db_file_dir + 'player_db_{}.json'

# name of the json file where the full player data is to be stored
player_full_db_file = player_db_file_dir + 'player_full_db.json'

# list of countries with their numeric code
country_list_db     = 'config_dir/country_code.json'

date_json_filename  = player_db_file_dir + 'all_event_time.json'
error_sleep_duration = 3

# ID of clans
clan_id_dict = { \
        'revo'  : {'clan_id':['93633','123276','119234'], 'clan_name':'DRIFT Revolutions'},
        'cyre'  : {'clan_id':['138751','190261'],         'clan_name':'Cyber Rebels Crew'},
        'espa'  : {'clan_id':['150634'],                  'clan_name':'Putos amos de ESP@'},
        'noss'  : {'clan_id':['188811'],                  'clan_name':'the brothers of ciro'},
        'sx'    : {'clan_id':['163287'],                  'clan_name':'Dirt Bikes'},
        'flux'  : {'clan_id':['178377'],                  'clan_name':'Outcasts'},
        'rush'  : {'clan_id':['50230'],                   'clan_name':'Rush Team Motori'},
        'vudu'  : {'clan_id':['164222','181859'],         'clan_name':'DARK ARTS RACING'},
        'free'  : {'clan_id':['----'],                    'clan_name':'Free agents'}}

clan_id_single_dict = { \
        'revo_main'     : {'clan_id':['93633'],  'clan_name':'DRIFT Revolutions',        'clan_tag':'REVO'},
        'revo_fresher'  : {'clan_id':['123276'], 'clan_name':'DRIFT Revolutions FRESHER','clan_tag':'RΕVO'},
        'revo_origins'  : {'clan_id':['119234'], 'clan_name':'DRIFT Revolutions ORIGINS','clan_tag':'REV0'},
        'cyre_main'     : {'clan_id':['138751'], 'clan_name':'Cyber Rebels Crew',        'clan_tag':'CYRE'},
        'espa'          : {'clan_id':['150634'], 'clan_name':'Putos amos de ESP@',       'clan_tag':'E$P@'},
        'noss'          : {'clan_id':['188811'], 'clan_name':'the brothers of ciro',     'clan_tag':'NOSS'},
        'sx'            : {'clan_id':['163287'], 'clan_name':'Dirt Bikes',               'clan_tag':'SX'},
        'flux'          : {'clan_id':['178377'], 'clan_name':'Outcasts',                 'clan_tag':'FLUX'},
        'rush'          : {'clan_id':['50230'],  'clan_name':'Rush Team Motori',         'clan_tag':'Rush'},
        'vudu'          : {'clan_id':['164222'], 'clan_name':'DARK ARTS RACING',         'clan_tag':'VUDU'},
        'p100'          : {'clan_id':['147490'], 'clan_name':'Poland 100 Years of Independance', 'clan_tag':'P100'},
        'cn_clan'       : {'clan_id':['187006'], 'clan_name':'Happy virus',              'clan_tag':'C҉N҉'},
        'swe'           : {'clan_id':['837'],    'clan_name':'Sweden',                   'clan_tag':'SWE'},
        'smiley'        : {'clan_id':['26498'],  'clan_name':'smiley',                   'clan_tag':'☺️'},
        'free'          : {'clan_id':['----'],   'clan_name':'Free agents',              'clan_tag':'----'}}

def col_header_key(req_type='public'):
    col_header_key = [ \
            'rank','name','user_id', \
            'country_id','clan_tag','trophies', \
            'leg_trophies','max_trophies','game_win', \
            'game_total','win_ratio','app_version','player_level']

    if req_type == 'private':
        col_header_key_private = [ \
                'time_played','num_purchase','diamonds','coins', \
                'gasoline','vip_level','vip_exp', \
                'acc_created','last_login']

        col_header_key += col_header_key_private

    return col_header_key

# List of all data fetched
# Used as column header in the full database webpage
col_header = { \
        'rank'          :['num_type','Rank'                      ],
        'clan_score'    :['num_type','Clan Score'                ],
        'name'          :['str_type','Username'                  ],
        'user_id'       :['num_type','Player ID'                 ],
        'country_id'    :['cen_type','Country'                   ],
        'clan_tag'      :['cen_type','Clan Tag'                  ],
        'clan_id'       :['num_type','Clan ID'                   ],
        'clan_name'     :['str_type','Clan Name'                 ],
        'trophies'      :['num_type','Trophies<br>(Current)'     ],
        'leg_trophies'  :['num_type','Trophies<br>(Legendary)'   ],
        'max_trophies'  :['num_type','Trophies<br>(Highest Ever)'],
        'game_win'      :['num_type','Matches Won'               ],
        'game_total'    :['num_type','Matches Played'            ],
        'win_ratio'     :['num_type','Win Ratio'                 ],
        'time_played'   :['cen_type','Time Played'               ],
        'num_purchase'  :['num_type','Number of<br>Purchases'    ],
        'diamonds'      :['num_type','Diamonds'                  ],
        'coins'         :['num_type','Coins'                     ],
        'gasoline'      :['num_type','Gasoline Buckets'          ],
        'vip_exp'       :['num_type','VIP<br>Experience'         ],
        'vip_level'     :['num_type','VIP<br>Level'              ],
        'player_level'  :['num_type','Level'                     ],
        'app_version'   :['cen_type','App Version'               ],
        'acc_created'   :['cen_type','Account<br>Created On'     ],
        'last_login'    :['cen_type','Account<br>Last Login'     ],
        'one_signal'    :['str_type','One Signal'                ],
        'device_id'     :['str_type','Device ID'                 ]}

# number of player details to be fetched per page
size_per_fetch = 200

# number of pages to be fetched for entire world
num_pages_fetch_world = 5

# number of pages to be fetched for a single country 
num_pages_fetch_country = 1

def country_db():
    import json
    country_dict = json.load(open(country_list_db,'r'))
    country_dict = {v: k for k, v in country_dict.items()}
    return country_dict

# list of countries from which data is to be fetched
def country_list():
    country_list = []
    country_list = [ \
                'au','nz', \
                'br','us','ca','mx', \
                'cn','in','id','kr','jp','sg','my','hk','th', \
                'pt','de','it','nl','fr','be','es','gb','ie','gr', \
                'pl','ro','si','hu', \
                'se','ch','no','ru','fi','dk']

    if is_heroku_env() is True:
        return country_list
    else:
        return country_list

# checking if app is running in local machine or heroku
def is_heroku_env():
    import os
    if 'DYNO' in os.environ:
        return True 
    else:
        return False

# sleep duration in seconds between two consecutive fetches
def fetch_interval():
    sleep_dur = 0
    if is_heroku_env() is True:
        sleep_dur = 1800
    else:
        sleep_dur = 600
    
    return sleep_dur


# season end date
season_end = {'dd':29,'mm':10,'yyyy':2019}

# number of entries to fetch while deep scanning
def full_detail_num_entries():
    num_fetch = 0
    if is_heroku_env() is True: 
        num_fetch = 1000
    else:
        num_fetch = 1000
    
    return num_fetch

empty_db = { \
        "server_started":"----",
        "before_ALL"    :"----",
        "after_ALL"     :"----",
        "before_country":"----",
        "after_country" :"----",
        "before_full"   :"----",
        "after_full"    :"----"}
