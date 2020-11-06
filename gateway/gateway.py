import json
import sys
import os
import shlex
import logging
import time
import discord
import aiohttp

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


async def generate_payload(message):
    """
    Generates a JSON-compatible payload to be sent to the backend
    
    The payload consists of six fields:
     - command: string, the one-word command string alone without the command
            prefix. The command is guaranteed to be in all lowercase letters
     - arguments: string array, every additional argument following the command. 
            This array will not include the command itself. Quoted substrings
            will be preserved.
     - user_id: long, the id of the user who sent the message
     - message_id: long, the id of the message itself
     - message_channel_id: long, the id of the message's channel
     - is_private: boolean, whether the channel is a private message

    For example, assuming the command prefix is '.', then the message content
        .choice first_choice "second choice" thirdChoice
    will generate the following fields in the payload:
    {
        command: "choice"
        arguments: ["first_choice", "second choice", "thirdChoice"]
    }

    If the message is of type string instead of type discord.Message, then
    the *_id fields and is_private field will be omitted

    Input parameters:
        message: a discord message received, or a raw string command
    Return type:
        dict: the payload generated (if message is a valid command)
        None: no available payload (if message is not a valid command)
    """
    payload = None
    content = ""
    if isinstance(message, discord.Message):
        content = message.content
    elif isinstance(message, str):
        content = message
    if content.startswith(client.command_prefix):
        content = content[1::] 
        content = shlex.split(content)
        payload = {
            "command": content[0].lower(),
            "arguments": content[1:],
        }
        if isinstance(message, discord.Message):
            payload["user_id"] = message.author.id
            payload["message_id"] = message.id 
            payload["message_channel_id"] = message.channel.id 
            payload["is_private"] = isinstance(message.channel, discord.abc.PrivateChannel)
        client.logger.debug(f"Built payload as {payload}")
    return payload


async def get_reply(url: str, payload: dict):
    """
    Gets the reply message from the URL for the given payload command

    The return dict has two fields, both of which may be empty strings:
     - response: string, the text response that should be sent
     - embed: string, the embed JSON that should be sent

    If the returned status code is not 200, response and embed will default to
    be empty strings

    The embed string should be a JSON-parsable string with fields as specified
    in the Discord documentation about embeds: 
    https://discord.com/developers/docs/resources/channel#embed-object

    Input parameters:
        url: string, the URL repsenting the backend to send to
        payload: dict, the payload to POST to the URL
    Return type:
        dict: the response
    """
    reply = {
        "response": "",
        "embed": ""
    }
    client.logger.debug(f"Sending command request to {url}: {payload}")
    try:
        start = time.perf_counter()
        async with client.aiohttp_session.post(url, json=payload) as r:
            if r.status == 200:
                js = await r.json()
                delta = round((time.perf_counter() - start) * 1000, 2)
                client.logger.info(f"Response received from backend in {delta} ms")
                reply["response"] = js.get("response", "")
                reply["embed"] = js.get("embed", "")
                client.logger.debug(f"Received reply from backend: {reply}")
            elif r.status == 204: # No command, swallow
                pass
            else:
                delta = (time.perf_counter() - start) * 1000
                client.logger.info(f"Got back response code {r.status} in {delta} ms")
    except aiohttp.ClientConnectorError as e:
        client.logger.warning("Could not connect to URL. Is it down?")
    return reply


@client.event
async def on_ready():
    """Fires when the bot is ready to process incoming messages"""
    client.aiohttp_session = aiohttp.ClientSession() # Must be in an async func
    client.logger.info("Logged in as %s (ID %s)", client.user.name, client.user.id)


@client.event
async def on_message(message):
    """Fires when any message is sent in a server the bot is in"""
    if message.author.id != client.user.id and not message.author.bot:
        payload = await generate_payload(message)
        if payload is not None:
            client.logger.debug("Command detected: " + payload["command"])
            url = "http://" + client.backend_addr + ":"
            url += client.backend_addr_port + "/command"
            reply = await get_reply(url, payload)
            response = reply["response"]
            embed = None
            try:
                embed = discord.Embed.from_dict(reply["embed"])
            except Exception as e: # Ignore if unparsable
                client.logger.debug(f"Error parsing embed: {e}")
            if response != "" or embed is not None: # We have something to send
                client.logger.debug(f"Sending the following: response {response} embed {embed}")
                try:
                    await message.channel.send(response, embed=embed)
                except discord.DiscordException as e:
                    client.logger.error("Error occurred sending message: " + str(e))


if __name__ == "__main__":
    client.logger.info("Initiating discord connection")
    client.run(client.bot_token, bot=True)
