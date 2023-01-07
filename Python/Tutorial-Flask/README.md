# Flask Tutorial
This folder contains various examples of flask apps. Each app folder has a `setup_env.sh` script that sets up the shell environment after which you can run `flask run` to start up the app.

## Overview
* **Flask** is a framework for building **Web Server Gateway Interface** (WSGI) web applications
* Flask website architecture for development mode
    * Based on application code, Flask sets up the web server, application server, and any databases before opening up a local port and managing HTTP communication over LAN. Any browser can be used to initiate a session with the Flask web server to request pages from the application. 
* Application factory - initialization function for the `Flask` application class
* Project layout
    * Flask can run an application based off a single file or a module (i.e folder with `__init__.py` defined a )
    * Instance folders vs root folder
        * runtime and configuration files used to be stored wherever developers wanted them to be and then could be accessed by a handle on the root folder. While this worked when running applications directly instead of as packages where the root folder is not the same as the application folder. A separate instance folder is now created to provide uniformity between both cases. The instance folder can be placed manually or left to Flask to add automatically.
* Routes - paths on the web server
    * Associating routes with functions
* Blueprints and View functions
    * View functions respond to client requests (i.e. GET) or submissions (i.e. POST) by telling flask what to do with user input, if it exists, and what to return to the user at the end of any processing. Flask handles the matching of view functions with specific URLs as well as generating the HTML that gets returned to the client browser
* Questions:
    * Is the flask functionality (e.g. validating user input) executed client side or server side?

## Flask code
Important globals:
* `g`
* `session`
* `request`
* `current_app`

Important classes:
* `Flask`
* `Blueprint`

Important functions:
* `url_for`
* `redirect`
* `render_template`
* `flash`

Interface functions (i.e. user defined but need a specific signature):
* `create_app`/`make_app` - for `project/__init__.py`

Common package extensions:
* `werkzeug.security`
* `click`
* `sqlite3`