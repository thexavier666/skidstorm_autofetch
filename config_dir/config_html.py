bgcolor_database    = '#ffffff'
bgcolor_body        = '#ffffff'

css_style_string = \
'''
.header{
	background: #3b5998;
	text-align: center;
	color: white;
}
.header-alt{
	background: #d9534f;
	text-align: center;
	color: white;
}
body{
	font-family: 'Space Mono', monospace;
	font-size: 12px;
}
.text-alt{
	font-family: 'Space Mono', monospace;
	font-size: 24px;
}
table{
	border:1px solid grey;
	margin-left:auto;
	margin-right:auto;
}
td.num_type{
	text-align: right;
}
td.cen_type{
        white-space: nowrap;
	text-align: center;
}
td.str_type{
	text-align: left;
        white-space: nowrap;
}
table td + td {
	border-left:1px solid gray;
}
.table-heading {
	border-bottom:1px solid gray;
	text-align:center;
        background:#3b79a9;
        color:#ffffff;
}
ul {
	display:table;
	margin:0 auto;
}
'''

style_string = \
'''
<head>
    <link href="https://fonts.googleapis.com/css?family=Space+Mono&display=swap" rel="stylesheet">
    <style>{}</style>
</head>
'''.format(css_style_string)

responsive_string = \
'''<meta name="viewport" content="width=device-width, initial-scale=1.0">'''

table_preamble = '''<table cellpadding="5">'''

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
    </body>
</html>
'''.format(responsive_string, style_string, bgcolor_body)

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
            <table>
                <tr>
                    <td class="table-heading"><b>Fetch Event</b></td>
                    <td class="table-heading"><b>Time of Event</b></td>
                </tr>
                <tr>
                    <td>Small database starts</td>
                    <td class="num_type">{}</td>
                </tr>
                <tr>
                    <td>Small database ends</td>
                    <td class="num_type">{}</td>
                </tr>
                <tr>
                    <td>Country database starts</td>
                    <td class="num_type">{}</td>
                </tr>
                <tr>
                    <td>Country database ends</td>
                    <td class="num_type">{}</td>
                </tr>
                <tr>
                    <td>Large database starts</td>
                    <td class="num_type">{}</td>
                </tr>
                <tr>
                    <td>Large database ends</td>
                    <td class="num_type">{}</td>
                </tr>
            </table>
        <center>
    </body>
</html>
'''
