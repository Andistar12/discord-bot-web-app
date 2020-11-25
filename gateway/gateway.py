import json
import sys
import os
import logging
import time
import discord
import aiohttp
import commands

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
RIOT_TOKEN = config.get("riot_token", None)
if RIOT_TOKEN is None:
    logging.error("Error: No riot games API token passed")
    sys.exit(1)
LOGGING_LEVEL = config.get("target", None)

# Create discord client
client = discord.Client()
client.bot_token = BOT_TOKEN
client.command_prefix = COMMAND_PREFIX
client.riot_token = RIOT_TOKEN

# Setup logging
logFormat = logging.Formatter(
    '[%(levelname)s] [%(name)s %(asctime)s] %(message)s')
consoleHandler = logging.StreamHandler(sys.stdout)
if isinstance(LOGGING_LEVEL, str) and LOGGING_LEVEL.startswith("prod"):
    consoleHandler.setLevel(logging.INFO)
else:
    consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(logFormat)
logging.getLogger().addHandler(consoleHandler)
logging.getLogger().setLevel(logging.DEBUG)
client.logger = logging.getLogger("gateway")


@client.event
async def on_ready():
    """Fires when the bot is ready to process incoming messages"""
    client.aiohttp_session = aiohttp.ClientSession() # Must be in an async func
    client.logger.info("Logged in as %s (ID %s)", client.user.name, client.user.id)


@client.event
async def on_message(message):
    """Fires when any message is sent in a server the bot is in"""
    if message.author.id != client.user.id and not message.author.bot:
        if message.content.startswith(client.command_prefix):
            start = time.perf_counter()
            cmd = commands.COMMAND(message)
            reply = cmd.execute()
            response = reply.get("response", "")
            embed = reply.get("embed", None)
            delta = (time.perf_counter() - start) * 1000
            if response != "" or embed is not None: # We have something to send
                client.logger.debug(f"Sending the following: response {response} embed {embed}")
                try:
                    await message.channel.send(response, embed=embed)
                    delta2 = (time.perf_counter() - start) * 1000
                    client.logger.info(f"Process command in {delta} ms, sent in {delta2} ms")
                except discord.DiscordException as e:
                    client.logger.error("Error occurred sending message: " + str(e))


if __name__ == "__main__":
    client.logger.info("Initiating discord connection")
    client.run(client.bot_token, bot=True)
