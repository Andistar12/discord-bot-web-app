import json
import sys
import os
import re
import logging
import discord
import aiohttp
import asyncio
import flask

# Load config file. Requires one env param "CONFIG_LOC"
try:
    CONFIG_LOC = os.environ.get("CONFIG_LOC", "/run/secret/config.json")
    cfgfile = open("./config.json")
    config = json.load(cfgfile)
except Exception as e:
    logging.critical("Error occurred opening config file config.json: " + str(e))
    sys.exit(1)

# Read in config file params
BOT_TOKEN = config.get("bot_token", None)
if BOT_TOKEN is None:
    logging.critical("Error: bot token is null")
    sys.exit(1)
COMMAND_PREFIX = config.get("command_prefix", None)
if COMMAND_PREFIX is None:
    logging.critical("Error: command prefix is null")
    sys.exit(1)
BACKEND_ADDR = config.get("backend_addr", None)
if BACKEND_ADDR is None:
    logging.critical("Error: backend address is null")
    sys.exit(1)
BACKEND_ADDR_PORT = config.get("backend_addr_port", None)
if BACKEND_ADDR_PORT is None:
    logging.critical("Error: backend address port is null")
    sys.exit(1)

# Create flask client
app = flask.Flask(__name__)
app.logger.setLevel(logging.DEBUG)

# Create discord client
client = discord.Client()
client.bot_token = BOT_TOKEN
client.command_prefix = COMMAND_PREFIX
client.backend_addr = BACKEND_ADDR
client.backend_addr_port = BACKEND_ADDR_PORT
client.logger = app.logger

# On ready - changes bot info as config requests
@client.event
async def on_ready():
    client.logger.info("Logged in as %s (ID %s)", client.user.name, client.user.id)


# General on message received, relayed to other commands
@client.event
async def on_message(message):
    if message.author.id != client.user.id and not message.author.bot:
        # Ignore messages from self and from bots
        if message.content.startswith(client.command_prefix):
            # Starts with prefix, process as command

            # Strip command prefix
            content = message.content[1::]
            # TODO verify that this actually splits correctly
            content = re.split(r'''((?:[^ "']|"[^"]*"|'[^']*')+)''', content)[1::2]
            command = content[1]
            arguments = content[1:]
            url = "http://" + client.BACKEND_ADDR + ":" + client.BACKEND_ADDR_PORT + "/command/" + command
            # Pass to backend
            payload = {
                "command": content[1],
                "arguments": content[1:],
                "user_id": message.author.id
            }
            client.logger.debug("Sending command request to backend: " + str(payload))
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=payload) as r:
                    if r.status == 200:
                        js = await r.json()
                        reply = js.get("response", None)
                        client.logger.debug("Received response: " + reply)
                        if isinstance(reply, str) and reply != "":
                            try:
                                await self.client.send_message(message.channel, reply)
                            except discord.DiscordException as e:
                                logger.info("Error occurred sending message: " + str(e))

@app.route("/bot/info")
def get_info():
    payload = {
        "username": etc,
        "command_prefix": etc
    }
    return flask.jsonify(payload), 200

@app.route("/bot/update", methods=["POST"])
def set_info():
    return flask.jsonify({}), 501 # TODO

def main():
    loop = asyncio.get_event_loop()
    client.logger.debug("Initiating discord bot")
    try:
        loop.run_until_complete(client.start(client.bot_token, bot=True))
    except Exception as e:
        client.logger.critical("Bot failed to start: " + str(e))
        sys.exit(1)
    client.logger.debug("Initiating flask api")
    app.run(port=5000, host="0.0.0.0")
    try:
        loop.run_until_complete(client.logout())
    except Exception as e:
        client.logger.warning("Bot failed to logout: " + str(e))
        sys.exit(1)
    loop.close()

if __name__ == "__main__":
    main()
