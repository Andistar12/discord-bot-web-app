import flask
import time
import logging
import sys
from flask import Flask, request, jsonify, Response
import json
import os

app = flask.Flask(__name__)

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
    RIOT_TOKEN = config.get("riot_token", None)
    if RIOT_TOKEN is None:
        logging.error("Error: No riot games API token passed")
        sys.exit(1)
    BACKEND_ADDR = config.get("backend_addr", None)
    if BACKEND_ADDR is None:
        logging.error("Error: No backend address given")
        sys.exit(1)
    BACKEND_ADDR_PORT = config.get("backend_addr_port")
    if BACKEND_PORT is None:
        logging.error("Error: No port given")
        sys.exit(1)

app.port = BACKEND_ADDR_PORT

@app.route("/commands", methods=['GET', 'POST'])
def get_all_commands():
    
    return

if __name__ == '__main__':
    app.run(port = app.port, host ="0.0.0.0", debug=True)