def start(site_title):
    """
    :param site_title: string to be the title of the HTML page, the default is eqaul to no page name
    :return: string containing HTML content
    """
    if not isinstance(site_title, str):
        raise TypeError("input must be a string")

    html_start = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <title>""" + site_title + """</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Roboto'>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <style>
    html,body,h1,h2,h3,h4,h5,h6 {font-family: "Roboto", sans-serif; color: #a3978f}
    body {background-color: #f3f2f1;}
    table, th, td {color:#e8e5e3; border: 1px solid black; border-collapse: collapse;}
    tr:nth-child(odd) {background-color: #990030;}
    tr:nth-child(even) {background-color: #a3978f;}
    </style>
    </head>
    <body class="w3-light-grey">

    <!-- Page Container -->
    <div class="w3-content w3-margin-top" style="max-width:1600px;">
    """
    return html_start


def h1(text):
    """
    :param h1: string with text for HTML header
    :return:  string containing HTML content
    """
    if not isinstance(text, str):
        raise TypeError("input must be a string")
    local_text = ("""<h1>""" + text + """</h1>
    """)
    return local_text


def h2(text):
    """
    :param h2: string with text for HTML header
    :return:  string containing HTML content
    """
    if not isinstance(text, str):
        raise TypeError("input must be a string")
    local_text = ("""<h2>""" + text + """</h2>
    """)
    return local_text


def h3(text):
    """
    :param h3: string with text for HTML header
    :return:  string containing HTML content
    """
    if not isinstance(text, str):
        raise TypeError("input must be a string")
    local_text = ("""<h3>""" + text + """</h3>
    """)
    return local_text


def para(text):
    """
    :param para: string with text for HTML paragraph
    :return:  string containing HTML content
    """
    if not isinstance(text, str):
        raise TypeError("input must be a string")
    local_text = ("""<p>""" + text + """</p>
    """)
    return local_text


def line_break():
    """
    :return:  string containing HTML content representing a line break
    """
    line_break = ("""<hr>
    """)
    return line_break


def end():
    """
    :return: string containing string representing the end of a HTML document
    """
    html_end = """
    </body>
    <!-- End Page Container -->
    </div>
    </html>"""
    return html_end


def np_matrix_as_table(array, headers=[], sides=[]):
    """
    :param array: numpy array to be displayed as a HTML table
    :param headers: table headers for columns, default is no headers
    :param sides: table headers for rows, default is no headers
    :return:
    """
    local_text = "<table style=\"width:80%\">"
    cols = array.shape[1]
    rows = array.shape[0]
    if headers != []:
        if sides != []:
            headers.insert(0, "-")
        local_text += "<tr>"
        for element in headers:
            local_text += "<th>"+element+"</th>"
        local_text += "</tr>"
    for i in range(rows):
        local_text += "<tr>"
        if sides != []:
            local_text += "<th>" + sides[i] + "</th>"
        for j in range(cols):
            local_text += "<td>" + str(array[i][j]) + "</td>"
        local_text += "</tr>"
    local_text += "</table>"

    return local_text


def plotly_figure(figure, id):
    """
    :param figure: plotly graph object or px figure
    :param id: unique id string of format 'id_number'
    :return:
    """
    json_figure = figure.to_json()
    html = """
        <div id="""+id+"""></div>
        <script>
            var plotly_data = {}
            Plotly.react("""+id+""", plotly_data.data, plotly_data.layout);
        </script>
    """
    local_text = html.format(json_figure)
    return local_text

def single_plotly_figure(site_title, figure):
    """
    :param figure: plotly graph object or px figure
    :return: html style string
    """
    if not isinstance(site_title, str):
        raise TypeError("input must be a string")

    json_figure = figure.to_json()
    html = """
        <div id="id_1"></div>
        <script>
            var plotly_data = {}
            Plotly.react("id_1", plotly_data.data, plotly_data.layout);
        </script>
    """
    graph_content = html.format(json_figure)

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <title>""" + site_title + """</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Roboto'>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <style>
    html,body,h1,h2,h3,h4,h5,h6 {font-family: "Roboto", sans-serif; color: #a3978f}
    body {background-color: #f3f2f1;}
    table, th, td {color:#e8e5e3; border: 1px solid black; border-collapse: collapse;}
    tr:nth-child(odd) {background-color: #990030;}
    tr:nth-child(even) {background-color: #a3978f;}
    </style>
    </head>
    <body class="w3-light-grey">

    <!-- Page Container -->
    <div class="w3-content w3-margin-top" style="max-width:1600px;">
    """
    html += graph_content
    html += """
    </body>
    <!-- End Page Container -->
    </div>
    </html>"""
    return html
