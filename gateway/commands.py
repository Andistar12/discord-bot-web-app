import time
import sys
import math
import datetime
import text_cmd
import discord
import shlex

class BOT:
    def __init__(self):
        self.text_cmd = text_cmd.TEXT()
        self.start_time = datetime.datetime.now()
        self.LOOK_UP = {"ping": self.text_cmd.ping, "pong": self.text_cmd.pong, "repeat": self.text_cmd.repeat, "eightball": self.text_cmd.eight_ball, 
                        "uptime": self.text_cmd.uptime, "choice": self.text_cmd.choice, "coinflip": self.text_cmd.coinflip, "randomcase": self.text_cmd.randomcase,
                        "maximize": self.text_cmd.maximize, "reverse": self.text_cmd.reverse, "gift": self.text_cmd.gift, "dice": self.text_cmd.dice}



class COMMAND(BOT):
    def __init__(self, message):
        super().__init__()
        content = message.content[1::] 
        content = shlex.split(content)
        
        self.command = content[0].lower()
        self.arguments = content[1:]
        self.user_id = message.author.id
        self.message_id = message.id
        self.message_ch_id = message.channel.id 
        self.is_priv = isinstance(message.channel, discord.abc.PrivateChannel)
        self.pack = {"command": self.command, "arguments": self.arguments, "user_id": self.user_id, "message_id": self.message_id, "message_channel_id": self.message_ch_id,
                "is_private": self.is_priv}


    def lookup(self, cmd):
        if cmd in self.LOOK_UP.keys():
            return True
        else:
            return False

    def execute(self):
        if self.lookup(self.command):
            return self.LOOK_UP[self.command](self.arguments, self.pack)
        elif self.lookup(self.command) == False:
            return ""
        else:
            return ""
    

