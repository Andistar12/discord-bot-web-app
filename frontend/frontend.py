import logging
import os
import sys
import json
import flask

# Third-party libraries
from flask import Flask, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from db import init_db_command
from user import User

try:
    CONFIG_PATH = os.environ.get("CONFIG_LOC", "config.json")
    cfgfile = open(CONFIG_PATH)
    config = json.load(cfgfile)
except Exception as error:
    logging.error("Error: unable to open config file: {error}".format(error = error))
    sys.exit(1)
if config is not None:
    BOT_TOKEN = config.get("bot_token", None)
    if BOT_TOKEN is None:
        logging.error("Error: No bot token passed")
        sys.exit(1)
    BACKEND_ADDR = config.get("backend_addr", None)
    if BACKEND_ADDR is None:
        logging.error("Error: No backend address given")
        sys.exit(1)
    BACKEND_ADDR_PORT = config.get("backend_addr_port", None)
    if BACKEND_ADDR_PORT is None:
        logging.error("Error: No port given")
        sys.exit(1)
    DISCORD_CLIENT_ID = config.get("discord_client_id", None)
    if DISCORD_CLIENT_ID is None:
        logging.error("Error: No discord client id given")
        sys.exit(1)
    DISCORD_CLIENT_SECRET = config.get("discord_client_secret", None)
    if DISCORD_CLIENT_SECRET is None:
        logging.error("Error: No discord client secret given")
        sys.exit(1)
    LOGGING_LEVEL = config.get("target", None)

app = flask.Flask(__name__)
app.backend_port = BACKEND_ADDR_PORT
app.backend_addr = BACKEND_ADDR
app.port = 1357 # TODO
app.config["SECRET_KEY"] = BOT_TOKEN

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

client = WebApplicationClient(DISCORD_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# TODO pull from backend
command_list = {
    "utilities": {
        "server": "Prints information about the current server the command was sent in. This command only works on servers, not DMs.<br><br>Command usage: <pre>server</pre>",
        "avatar": "Displays the avatar of the bot, or a target user if somebody is @ mentioned.<br><br>Command usage: <pre>avatar [target]</pre>"
    },
    "anime": {
        "anime": "no anime",
        "waifu": "waifu todo",
        "headpat": "todo headpat"
    }
}

# TODO do something about this
main_nav_bar = [
    # href, page id, page title
    ("/", "status", "Status"),
    ("/commands", "commands", "Commands"),
    ("/login", "login", "Login")
]
admin_nav_bar = [
    # href, page id, page title
    ("/", "status", "Status"),
    ("/commands", "commands", "Commands"),
    ("/admin/manage", "manage", "Manage"),
    #("/admin/servers", "servers", "Servers"),
    #("/admin/logs", "logs", "Logs"),
    #("/admin/cadvisor", "cadvisor", "CAdvisor"),
    #("/admin/adminer", "adminer", "Adminer"),
    ("/logout", "logout", "Logout")
]

@app.route("/admin/manage", methods=["GET"])
def manage():
    return flask.render_template("manage.html", nav_bar=admin_nav_bar)

@app.route("/", methods=["GET"])
def status():
    return flask.render_template("status.html", nav_bar=main_nav_bar,
            username="Korone-chan")

@app.route("/commands", methods=["GET"])
def commands():
    return flask.render_template("commands.html", nav_bar=main_nav_bar, commands=command_list)

@app.route("/login")
def login():
    request_uri = client.prepare_request_uri(
        "https://discord.com/api/oauth2/authorize",
        redirect_url=request.base_url + "/callback",
        scope=["identify"]
    )
    return redirect(request_url)

@app.route("/login/callback", methods=["GET"])
def login_callback():
    code = request.args.get("code")

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        "https://discord.com/api/oauth2/token",
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Get user info
    userinfo_endpoint = "https://discord.com/api/users/@me"
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    user = userinfo_response.json()
    user_id = user["id"]
    username = user["name"]

    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == '__main__':
    debug = False
    if LOGGING_LEVEL == "debug" or LOGGING_LEVEL == "dev":
        debug = True
    app.run(port = app.port, host ="0.0.0.0", debug=debug)
