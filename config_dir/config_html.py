style_string = \
"<head> \
    <link href=\"https://fonts.googleapis.com/css?family=Roboto+Mono&display=swap\" rel=\"stylesheet\"> \
    <style> \
        body{ \
            font-family: 'Roboto Mono', monospace; \
            font-size: %dpx; \
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

responsive_string = "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"

table_preamble = '<table cellpadding=\"5\">'

bgcolor_clan        = '#98c4ff'
bgcolor_season_end  = '#e0a899'
bgcolor_database    = '#ffc0cb'
bgcolor_error       = '#e35604'

full_db_error = \
"<html> \
    {} \
    <body bgcolor=\"{}\"> \
        <center> \
        <br><br> \
        <h2>⚠ ERROR ⚠</h2> \
        😱 Oh no! 😱<br> \
        The page is still being baked 👩‍🍳 <br> \
        😞 Come back after some time 😞\
        </center> \
    </body> \
</html>".format(style_string % (36), bgcolor_error)
