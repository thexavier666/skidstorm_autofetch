# directory in which the fetched data is to be stored
player_db_file_dir  = 'data/'

# name of the json file where the data is to be stored
player_db_file      = player_db_file_dir + 'player_db_{}.json'

# name of the json file where the full player data is to be stored
player_full_db_file = player_db_file_dir + 'player_full_db.json'

# list of countries with their numeric code
country_list_db     = 'public/country_code.json'

# ID of clans
clan_id_dict = {
        'revo' : ['93633','123276','119234','126321'],
        'cyre' : ['138751','190261'],
        'espa' : ['150634'],
        'noss' : ['188811'],
        'sx'   : ['163287'],
        'flux' : ['178377'],
        'rush' : ['50230'],
        'vudu' : ['164222','181859'],
        'free' : ['0']}

# number of pages to be fetched for entire world
num_pages_fetch_world = 11

# number of pages to be fetched for a single country 
num_pages_fetch_country = 1

# sleep duration in seconds between two consecutive fetches
fetch_interval = 120
fetch_interval_big_db = 1800

# list of countries from which data is to be fetched
country_list = [  'au', \
        'br','us','ca','mx', \
        'cn','in','id','kr','jp', \
        'pt','de','pl','it','se','nl','fr','be','es','gb']

# number of player details to be fetched per page
size_per_fetch = 100

# season end date
season_end = {'dd':29,'mm':10,'yyyy':2019}

# number of entries to fetch while deep scanning
full_detail_num_entries = 200 
