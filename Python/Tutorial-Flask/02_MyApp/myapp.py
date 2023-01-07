################################################################################
# NOTES:
# Testing your understanding with this tutorial requires starting up a web
# server and then manually visiting the routed URLs to check for expected output
################################################################################
from datetime import datetime
import flask
from flask.json import dump

import os

app = flask.Flask(
    __name__,
    static_folder='my_statics',
    template_folder='my_templates',
    instance_path='/my_instance', instance_relative_config=True,
    )
app.config.from_mapping(SECRET_KEY='dev') # needed for session global

################################################################################
# Add views (a.k.a. web pages)
################################################################################
def my_view_func():
    return "Hello, World!"

# Create rule binding view function to a specific URL
app.add_url_rule("/view1", view_func=my_view_func) # Accessed as "URL/view1"

# Route URL to view function with a decorator
# - the decorator tells @app that whenever a user visits our app 
#   domain (myapp.com) at the given .route(), execute the following view 
#   function
@app.route('/view2')
def my_view_func2():
    return "View function routed with decorator that uses add_url_rule"

# Route multiple URLs to the same view function
@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    links = [
        flask.url_for('my_view_func'),
        flask.url_for('my_view_func2'),
        flask.url_for('canonical'),
        flask.url_for('print_string', string='my_string'),
        flask.url_for('print_int', num=1),
        flask.url_for('print_float', num=1.1),
        flask.url_for('print_text',text='my_text'),
        flask.url_for('http_request'),
        flask.url_for('generate_html'),
        flask.url_for('mysession'),
        flask.url_for('end_mysession'),
        flask.url_for('cookie'),
        flask.url_for('abort_code', code='404'),
        flask.url_for('static_image'),
        flask.url_for('matplotlib_png'),
        flask.url_for('matplotlib_attach'),
        flask.url_for('matplotlib_embed'),
        flask.url_for('send_plotly'),
    ]

    rv = '<h1>home page</h1>'
    rv += '<p> Try the following links'
    rv += '<ul>'
    for l in links:
        path = f'http://localhost:5000{l}'
        rv += f'<li><a href="{path}">{path}</a></li>'
    rv += '</ul></p>'

    return rv

# Canonical URL
@app.route('/canonical/')
def canonical():
    return "This page can be accessed as /canonical or /canonical/"

# Route to URL with variable
@app.route('/print_string/<string>')
def print_string(string):
    return f"String = '{string}'"

@app.route('/print_int/<int:num>')
def print_int(num):
    return f"Integer = {num} &rarr; Integer^2 = {num**2}"

@app.route('/print_float/<float:num>')
def print_float(num):
    # 404 error if num is an integer
    return f"Float = {num} &rarr; Float/3 = {num/3}"

# Redirect to other URLs and view functions
@app.route('/print/<text>')
def print_text(text):
    if text.isdigit():
        url = flask.url_for('print_int', num=text)
        return flask.redirect(url)
    try:
        f = float(text)
        url = flask.url_for('print_float', num=text)
        return flask.redirect(url)
    except ValueError:
        pass
    url = flask.url_for('print_string', string=text)
    return flask.redirect(url)

################################################################################
# Responding to different HTTP methods
# Open up app_requests.html in browser to test this
################################################################################
@app.route('/http_request', methods=['GET', 'POST'])
# If the method isn't specified: "Method Not Allowed" error returned to user
def http_request():
    if flask.request.method == "GET" and not flask.request.args:
        return flask.send_from_directory('my_statics','app_requests.html')

    rv = f"""
    <html>
    <head>
        <title>HTTP Request Test</title>  
    </head>
    <body>
    <h1>User Request Summary</h1>
    <pre>
        request.method  = {repr(flask.request.method)}
        request.args    = {repr(flask.request.args)}
        request.form    = {repr(flask.request.form)}
        request.cookies = {repr(flask.request.cookies)}
        request.files   = {repr(flask.request.files)}
    </pre>
    </body>
    </html>
    """
    return rv

################################################################################
# Accessing content through local paths and URLs
################################################################################
# url_for 
# - maps view-function endpoint names to the url stored in app
# - access static files relative to the 'static/' folder
# - dot (.) separators and blueprints

# render_template
# - access Jinja templates relative to the 'templates/' folder

# open_resource - open() but relative to app.root_path
# open_instance_resource = open() but relative to app.instance_path

################################################################################
# Building web pages from templates
################################################################################
@app.route('/jinja_template')
def generate_html():
    myvar = 'val'
    mylist = [1,2,[9,8],3,4]
    mydict = {
        "key1" : 1,
        "key2" : "text"
    }
    return flask.render_template('jinja_template.html', myvar=myvar, mydict=mydict, mylist=mylist)

################################################################################
# Sessions and Cookies
# - Similar functionality but session storage preferred
# - Session data is encoded and can't be modifed by user while cookies can
# - Session data should be small so larger data should be stored server side and
#   referenced with a key stored in the session data
################################################################################
@app.route('/mysession')
def mysession():
    if 'start_time' not in flask.session:
        flask.session['start_time'] = datetime.now()
    return f"<h1>Session start time : {flask.session['start_time']}</h1>"

@app.route('/end_mysession')
def end_mysession():
    start_time = flask.session.pop('start_time', None)
    if start_time is None:
        return f"<h1>Session never started. Visit /mysession first</h1>"
    return f"<h1>Length of session : {datetime.now() - start_time}"

@app.route('/cookie')
def cookie():
    # Get cookie from browser request
    if (n_visits := flask.request.cookies.get('n_visits')) is None:
        n_visits = 1
    
    # Set/Update cookie for response
    html_text = f"<h1> Number of visits to this page: {n_visits}</h1>"
    resp = flask.make_response(html_text)
    resp.set_cookie('n_visits', str(int(n_visits)+1))
    return resp

################################################################################
# Status codes
# - Is using the exact right status code important? Not really
# - see: https://stackoverflow.com/questions/62254230/why-and-how-http-responses-status-code-matter
################################################################################
@app.route('/abort-<code>')
def abort_code(code):
    if code in ['400','401','403','404','406','415','429']:
        flask.abort(int(code))
    else:
        return "<h1>Unknown abort code : " + code + "</h1>"

################################################################################
# Flash messages and logging
################################################################################

################################################################################
# Returning images
################################################################################
# Static images
@app.route('/static_image')
def static_image():
    # Paths that work
    path = flask.url_for('static', filename='Flask_logo.png')
    #path = app.static_url_path + '/Flask_logo.png'
    #path = 'my_statics/Flask_logo.png'

    # Paths that DONT work
    #path = flask.url_for('my_statics', filename='Flask_logo.png')
    #path = app.static_folder + '/Flask_logo.png'

    return f'''
    <h1>Static Image</h1> 
    <img src="{path}" style="max-width:100%"/> 
    <p>src="{path}"</p>'''


# Generated images
# - DONT USE pyplot. It will cause crashes because it tries maintaining
#   references to figures that go out of scope.
# - Use Object-Oriented style instead
# - Setting matplotlib backend (e.g. Agg) seems to allow using pyplot

# Matplotlib/Seaborn
import io
#import matplotlib; matplotlib.use("Agg")
#import matplotlib.pyplot as plt; 
from matplotlib.figure import Figure

def get_matplotlib_fig():
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1,3,2,5,4])
    return fig

def matplotlib_fig_to_bytes(fig):
    data_bytes = io.BytesIO()
    fig.savefig(data_bytes, format='png')
    
    # I see these in examples but seem unnecessary
    #data_bytes.seek(0)
    #return data_bytes.getvalue()

    return data_bytes

import base64
def bytes_to_base64(data_bytes):
    # byte-stream -> bytes-like object
    buf = data_bytes.getbuffer()
    # bytes-like object -> base64 (i.e. 6-bit) binary
    data_base64_bin = base64.b64encode(buf)
    # base64 binary -> base64 ASCII
    data_base64_ascii = data_base64_bin.decode('ascii')

    return data_base64_ascii

# Send image directly (can be type other than png)
@app.route('/matplotlib.png')
def matplotlib_png():
    fig = get_matplotlib_fig()
    filename = 'matplotlib.png'
    
    # Two options for sending files
    # 1) Send directly a locally stored file
    save_path = os.path.join(app.static_folder, filename)
    fig.savefig(save_path)
    # Less secure if save_path not trusted
    #return flask.send_file(save_path)
    #return app.send_static_file(filename)
    # Safety checks on file path being requested
    return flask.send_from_directory(app.static_folder, filename)
    
    # 2) Send directly a bytes stream 
    data_bytes = matplotlib_fig_to_bytes(fig)
    return flask.send_file(data_bytes,
                           attachment_filename=filename,
                           mimetype='image/png')

# Send HTML that downloads image
# - Requires view function that sends file
@app.route('/matplotlib_attach')
def matplotlib_attach():
    image_url = flask.url_for('matplotlib_png', _external=True) # absolute url
    #image_url = flask.url_for('matplotlib_png') # relative url
    
    return f'''
    <h1> Download image within HTML </h1>
    <img src="{image_url}"/>
    <p>Downloaded image url = {image_url} </p>
    '''

# Embed image in-line using data URI scheme
# - data URI syntax : data:[<media type>][;base64],<data>
# - media type = MIME syntax: type/subtype (e.g. image/png, video/mp4, text/csv)
@app.route('/matplotlib_embed')
def matplotlib_embed():
    fig = get_matplotlib_fig()
    data_bytes = matplotlib_fig_to_bytes(fig)
    data_base64 = bytes_to_base64(data_bytes)
    n = len(data_base64)
    return f'''
    <h1> Embedded image using data URI </h1>
    <img src="data:image/png;base64,{data_base64}"/>
    <p style="word-wrap:break-word">Image Data ({n} chars) = <br>{data_base64}</p>
    '''

# Plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import json
def get_plotly_data():
    return px.line(y=[1,3,2,4,6,5,10])

# Send json-encoded image and plot in HTML using JS
@app.route('/plotly')
def send_plotly():
    fig = get_plotly_data()
    div_id = 'plotly'
    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder, indent=4)
    return f'''
        <h1> Plotly plot </h1>
        <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
        <div id='{div_id}'>
        <script>
            Plotly.newPlot('{div_id}', {graphJSON})
        </script>
        <p>
        Plotly JSON data
        <br>
        <pre>{graphJSON}</pre>
        </div>
    '''

# Bokeh

# Altair

# d3

################################################################################
# File uploading
################################################################################

################################################################################
# Application and Request contexts
################################################################################

################################################################################
# Teardown functions
################################################################################

################################################################################
# Unit Testing (see tests/)
################################################################################

################################################################################
# Handling and Debugging Application Errors
################################################################################

################################################################################
# Logging
################################################################################

################################################################################
# Blueprints
################################################################################

################################################################################
# Add custom flask CLI commands
# - useful for actions occuring before or after running the application such as
#   initializing/updating a database (anything else?)
################################################################################
# @click.command('my-cmd')
# @flask.with_appcontext
# def cmd():
#   ...
# app.cli.add_command(cmd)

################################################################################
# Advanced Topics
################################################################################
# Configuration

# Signals

# Pluggable Views


################################################################################
# Questions
# - How do app and session context work? What can and cannot be done inside and 
#   outside those contexts? How do you use with_appcontext properly?
#
# - How do the various functions handle finding files? When is abs path or rel 
#   path required? When does it assume a given project dir structure? 
