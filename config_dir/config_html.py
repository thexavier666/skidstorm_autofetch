bgcolor_database    = '#ffffff'
bgcolor_body        = '#ffffff'

list_to_html_country_header = \
'''
<div class="header">
    <br>
    <h1>Country Rank</h1>
    <br>
</div>
<br>
'''

list_to_html_clan_rank_header = \
'''
<div class="header">
    <br>
    <h1>Clan Rank</h1>
    <br>
</div>
<br>
'''

style_string = \
'''
<head>
    <link href="https://fonts.googleapis.com/css?family=Space+Mono&display=swap" rel="stylesheet">
    <link href="/stylesheet-alt.css" rel="stylesheet">
</head>
'''

responsive_string = \
'''<meta name="viewport" content="width=device-width, initial-scale=1.0">'''

table_preamble = '''<table cellpadding="5">'''

page_ending = \
'''
<div class="alt-footer">
	<br>
	<h2><a href="/" style="text-decoration:none">🏠</a></h2>
	<br>
	<br>
	If you want to donate, 
	you can Paypal at 
	<a href="https://paypal.me/thexavier666">thexavier666</a>
	<br>
	<br>
	<i>Brought to you by xavier666 ❤️</i>
</div>
'''

possible_clan_score = \
'''
<html>
    {}{}
    <body bgcolor={}>
        <div class="header-alt">
            <br>
            <h1>Calculate Dream Team Score</h1>
            <br>
        </div>
        <br>
        <div class="text-alt">
            <ul>
                <li>Enter the player IDs in a list format</li>
                <li>Do not use comma or extra space around the IDs</li>
                <li>Find the full list of IDs <a href="/gen/get_full_details">here</a></li>
                <li>Enter the player IDs in the order of their RANKS</li>
            </ul>
        </div>
        <br>
        <br>
        <center>
            <form action="/secret/do_clan_score" method="POST">
            <textarea rows="20" cols="30" name="player_id_list"></textarea>
            <br>
            <br>
            <input value="Calculate Score" type="submit" />
            </form>
        </center>
        {}
    </body>
</html>
'''.format(responsive_string, style_string, bgcolor_body, page_ending)

season_end_string = \
'''
<html>
    {}{}
    <body bgcolor="{}">
        <div class="header">
            <br>
            <h1>Season End Status</h1>
            <br>
        </div>
        <center> 
            <br><br>
            <h1>Season ends in</h1>
            <h2>{} days</h2>
            <h1>which is on</h1>
            <h2>{} GMT</h2>
        <center>
        {}
    </body>
</html>
'''

date_file_string = \
'''
<html>
    {}{}
    <body bgcolor="{}">
        <div class="header">
            <br>
            <h1>Webapp Update Status</h1>
            <br>
            <h3>Current time is : {}</h3>
            <h3>Server ON since : {}</h3>
            <br>
        </div>
        <br>
        <center> 
            <br>
            <table cellpadding="5">
                <tr>
                    <td class="table-heading"><b>Fetch Event</b></td>
                    <td class="table-heading"><b>Time of Event</b></td>
                </tr>
                <tr>
                    <td>Small database starts</td>
                    <td class="str_type">{}</td>
                </tr>
                <tr>
                    <td>Small database ends</td>
                    <td class="str_type">{}</td>
                </tr>
                <tr>
                    <td>Country database starts</td>
                    <td class="str_type">{}</td>
                </tr>
                <tr>
                    <td>Country database ends</td>
                    <td class="str_type">{}</td>
                </tr>
                <tr>
                    <td>Large database starts</td>
                    <td class="str_type">{}</td>
                </tr>
                <tr>
                    <td>Large database ends</td>
                    <td class="str_type">{}</td>
                </tr>
            </table>
        <center>
        {}
    </body>
</html>
'''
