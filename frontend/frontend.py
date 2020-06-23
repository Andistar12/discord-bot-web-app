import flask
import logging
import os
import sys
import json

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
    BACKEND_ADDR_PORT = config.get("backend_addr_port")
    if BACKEND_ADDR_PORT is None:
        logging.error("Error: No port given")
        sys.exit(1)
    LOGGING_LEVEL = config.get("target", None)

app = flask.Flask(__name__)
app.backend_port = BACKEND_ADDR_PORT
app.backend_addr = BACKEND_ADDR
app.port = 1357 # TODO
app.config["SECRET_KEY"] = BOT_TOKEN

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

@app.route("/", methods=["GET"])
def status():
    logged_in = False
    return flask.render_template("status.html", logged_in=logged_in)

@app.route("/commands", methods=["GET"])
def commands():
    logged_in = False
    return flask.render_template("commands.html", logged_in=logged_in, commands=command_list)

if __name__ == '__main__':
    debug = False
    if LOGGING_LEVEL == "debug" or LOGGING_LEVEL == "dev":
        debug = True
    app.run(port = app.port, host ="0.0.0.0", debug=debug)