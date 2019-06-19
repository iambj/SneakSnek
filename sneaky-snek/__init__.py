import os, time
from datetime import datetime
from colorama import Fore, Back, Style
import flask
from flask import request
# provides helper functions throughout the app and templates.
from hippo_server.helpers import Helpers
helpers = Helpers()

from hippo_server.watchFolders import Watcher, Handler

from flask import Flask, url_for, render_template, redirect


colors = {
    'clear' : "\033[0m'"
}

def printc(color, msg, type=None):
    print(Fore.YELLOW + msg + Style.RESET_ALL)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )
    print(f"App started on {helpers.get_short_date()}")

    if test_config is None:
        # load the instance config, if it exists, when not testing. 
        try:
            app.config.from_pyfile('config1.py', silent=False) 
            # config file is a .py and just assign variables.
        except FileNotFoundError:
            printc("yellow" , "INFO: Config file was not found. Using development defaults | Key:" + app.config['SECRET_KEY'])
        else:
            print(Fore.YELLOW + "INFO: Using config file!", Style.RESET_ALL)     
            print(app.config['SECRET_KEY'])       
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        printc("yellow", "INFO: Using 'test_config'.")
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError as e:
        print(Fore.YELLOW + "INFO: Error creating instance folder:", e, Style.RESET_ALL)
        pass

    @app.context_processor
    def inject_dict_for_all_templates():
        return dict(helpers=helpers)



    # This should be fixed up and have nginx serve
    @app.route("/favicon.ico")
    def favicon():
        return "Not found.", 404


    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # Home route
    @app.route("/ping")
    def ping():
        string = "instance_path: {}".format(app.instance_path)
        string += "</br>app: {}".format(app)
        # return string
        # return url_for('static', filename='home.html')
        # return render_template("home.html")
        return f'Pong! But it\'s {helpers.get_year()}.'
    # @app.route("/login")
    # def login():
    #     return redirect(url_for('auth.login'))
    
	#watchFolders
    @app.route("/newshit", methods=["GET", 'POST'])
    def newshit():
        return Handler.handle_request(app, bytes.decode(request.data))
        
### tes

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    
    from . import comingsoon
    app.register_blueprint(comingsoon.bp)

    Handler.make_new_shit(app)  #watchFolders



    return app
