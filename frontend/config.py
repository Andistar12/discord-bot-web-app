import os
import sys
import json
import logging
from datetime import timedelta

try:
    config_loc = os.environ.get("CONFIG_LOC", "config.json")
    with open(config_loc) as f:
        config = json.load(f)
except Exception as error:
    logging.error("Error: unable to open config file: {}".format(error))
    sys.exit(1)
if config is not None:
    BOT_TOKEN = config.get("bot_token", None)
    if BOT_TOKEN is None:
        logging.error("Error: No bot token passed")
        sys.exit(1)
    COMMAND_PREFIX = config.get("command_prefix", None)
    if COMMAND_PREFIX is None:
        logging.critical("Error: command prefix is null")
        sys.exit(1)
    BACKEND_ADDR = config.get("backend_addr", None)
    if BACKEND_ADDR is None:
        logging.error("Error: No backend address given")
        sys.exit(1)
    BACKEND_PORT = config.get("backend_addr_port", None)
    if BACKEND_PORT is None:
        logging.error("Error: No backend port given")
        sys.exit(1)
    FRONTEND_PORT = config.get("frontend_port", None)
    if FRONTEND_PORT is None:
        logging.error("Error: No frontend port given")
        sys.exit(1)
    REDIS_ADDR = config.get("redis_addr", None)
    if REDIS_ADDR is None:
        logging.error("Error: no reddis address given")
        sys.exit(1)
    REDIS_PORT = config.get("redis_port", None)
    if REDIS_PORT is None:
        logging.error("Error: no reddis port given")
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
    ADMIN_LIST = config.get("admin_list", "")

SECRET_KEY = BOT_TOKEN
REMEMBER_COOKIE_HTTPONLY = True

DISCORD_API_BASE = "https://discord.com/api/v6"
DISCORD_API_AUTHORIZE = "/oauth2/authorize"
DISCORD_API_TOKEN = "/oauth2/token"
DISCORD_API_TOKEN_REVOKE = "/oauth2/revoke"
DISCORD_API_USERS_ME = "/users/@me"
DISCORD_CDN_BASE = "https://cdn.discordapp.com/"
