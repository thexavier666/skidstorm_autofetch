bgcolor_clan        = '#98c4ff'
bgcolor_season_end  = '#e0a899'
bgcolor_database    = '#ffc0cb'
bgcolor_clan_score  = '#c7b1ac'

style_string = \
'''
<head>
    <link href="https://fonts.googleapis.com/css?family=Roboto+Mono&display=swap" rel="stylesheet">
    <style>
        body{
            font-family: 'Roboto Mono', monospace;
            font-size: %dpx;
        }
        table{
            border:1px solid grey;
            margin-left:auto;
            margin-right:auto;
        }
        td.num_type{
            text-align: right;
        }
        table td + td {
            border-left:1px solid gray;
        }
        .table-heading {
            border-bottom:1px solid gray;
            text-align:center;
        }
        ul {
            display:table;
            margin:0 auto;
        }
    </style>
</head>
'''

responsive_string = "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"

table_preamble = '<table cellpadding=\"5\">'

possible_clan_score = \
'''
<html>
    {}{}
    <body bgcolor={}>
        <br>
        <br>
        <h2><center>Calculate Dream Team Score</center></h2>
        <ul>
            <li>Enter the player IDs in a list format</li>
            <li>Do not use comma or extra space around the IDs</li>
            <li>Find the full list of IDs <a href="/gen/get_full_details">here</a></li>
        </ul>
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
    </body>
</html>
'''.format(responsive_string, style_string % 24, bgcolor_clan_score)

season_end_string = \
'''
<html>
    {}
    <body bgcolor="{}">
        <center> 
            <br><br>
            Season ends in
            <br><br><b>
            {} days
            </b><br><br>
            which is on
            <br><br><b>
            {} GMT
            </b>
        <center>
    </body>
</html>
'''
