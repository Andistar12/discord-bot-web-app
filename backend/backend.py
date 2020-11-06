import json
import os
import time
import sys
import flask
import logging
from flask import Flask, request, jsonify, Response


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
    if BACKEND_ADDR_PORT is None:
        logging.error("Error: No port given")
        sys.exit(1)
    LOGGING_LEVEL = config.get("target", None)

app = flask.Flask(__name__)
app.port = BACKEND_ADDR_PORT
app.backend_addr = BACKEND_ADDR

@app.route("/commands", methods=['GET'])
def get_all_commands():
    """Endpoint that returns all commands"""
    response = {
        "commands": ["ping", "repeat"]
    }
    return jsonify(response)


@app.route("/command", methods=["POST"])
def process_command():
    """Endpoint that processes a single Discord command message"""
    command = request.json.get("command", "")

    if command == "ping":
        response = {"response": "Pong!"}
        return jsonify(response)
    elif command == "pong":
        response = {"response": "Ping!"}
        return jsonify(response)
    elif command = "repeat":
        args = request.json.get("arguments", [])
        response = {
            "response": "Specify something for me to repeat!"
        }
        if len(args) > 0:
            response["response"] = " ".join(args)
        return jsonify(response)

    abort(404)

if __name__ == '__main__':
    debug = False
    if LOGGING_LEVEL == "debug" or LOGGING_LEVEL == "dev":
        debug = True
    app.run(port = app.port, host ="0.0.0.0", debug=debug)
