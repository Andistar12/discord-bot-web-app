import json
import sys
import os
import re
import logging
import discord
import aiohttp
import async_timeout

# Load config file. Requires one env param "CONFIG_LOC"
try:
    CONFIG_LOC = os.environ.get("CONFIG_LOC", "/run/secret/config.json")
    cfgfile = open(CONFIG_LOC)
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
LOGGING_LEVEL = config.get("target", None)

# Create discord client
client = discord.Client()
client.bot_token = BOT_TOKEN
client.command_prefix = COMMAND_PREFIX
client.backend_addr = BACKEND_ADDR
client.backend_addr_port = BACKEND_ADDR_PORT

# Setup logging
client.logger = logging.getLogger("gateway")
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
if isinstance(LOGGING_LEVEL, str) and LOGGING_LEVEL.startswith("prod"):
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.getLogger.setLevel(logging.DEBUG)

# Create aiohttp session
session = aiohttp.ClientSession()

# On ready - changes bot info as config requests
@client.event
async def on_ready():
    client.logger.info("Logged in as %s (ID %s)", client.user.name, client.user.id)

# On message received, calls the backend
@client.event
async def on_message(message):
    if message.author.id != client.user.id and not message.author.bot:
        # Ignore messages from self and from bots
        if message.content.startswith(client.command_prefix):
            client.logger.debug("Command detected: " + message.content)
            # Starts with prefix, process as command

            # Strip command prefix, split arguments, form payload
            content = message.content[1::]
            content = re.split(r'''((?:[^ "']|"[^"]*"|'[^']*')+)''', content)[1::2]
            command = content[0]
            arguments = content[1:]
            url = "http://" + client.backend_addr + ":" + client.backend_addr_port + "/command/" + command.lower()
            # Pass to backend
            payload = {
                "command": command,
                "arguments": arguments,
                "user_id": message.author.id,
                "message_id": message.id,
                "message_channel_id": message.channel.id
            }

            client.logger.debug(f"Sending command request to {url}: {payload}")
            async with session.post(url, json=payload) as r:
                client.logger.info("Response received")
                if r.status == 200:
                    js = await r.json()
                    reply = js.get("response", None)
                    client.logger.debug("Received response: " + reply)
                    if isinstance(reply, str) and reply != "":
                        try:
                            await message.channel.send(reply)
                        except discord.DiscordException as e:
                            client.logger.error("Error occurred sending message: " + str(e))
                else:
                    client.logger.info(f"Got back response code {r.status}")

if __name__ == "__main__":
    client.logger.info("Initiating discord connection")
    client.run(client.bot_token, bot=True)
