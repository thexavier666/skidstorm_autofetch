style_string = \
"<head> \
    <link href=\"https://fonts.googleapis.com/css?family=Roboto+Mono&display=swap\" rel=\"stylesheet\"> \
    <style> \
        body{ \
            font-family: 'Roboto Mono', monospace; \
            font-size: %dpx; \
        } \
        table{ \
            border:1px solid grey; \
            margin-left:auto; \
            margin-right:auto; \
        } \
        td.num_type{ \
            text-align: right; \
        } \
        table td + td { \
            border-left:1px solid gray; \
        } \
        .table-heading { \
            border-bottom:1px solid gray; \
            text-align:center; \
        } \
        ul { \
            display:table; \
            margin:0 auto; \
        } \
    </style> \
</head>"

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
            <li>Enter the player ID's in a list</li>
            <li>Do not use comma</li>
            <li>Do not use extra space around the name</li>
        </ul>
        <br>
        <br>
        <center>
            <form action="/secret/do_clan_score" method="POST">
            <textarea rows="20" cols="100" name="player_id_list"></textarea>
            <br>
            <br>
            <input value="Calculate Score" type="submit" />
            </form>
        </center>
    </body>
</html>
'''.format(responsive_string, style_string % 24, "#c7b1ac")

bgcolor_clan        = '#98c4ff'
bgcolor_season_end  = '#e0a899'
bgcolor_database    = '#ffc0cb'
