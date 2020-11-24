import time
import sys
import math
import datetime
import text_cmd


class BOT:
    def __init__(self):
        self.text_cmd = text_cmd.TEXT()
        self.start_time = datetime.datetime.now()
        self.LOOK_UP = {"ping": self.text_cmd.ping, "pong": self.text_cmd.pong, "repeat": self.text_cmd.repeat, "eightball": self.text_cmd.eight_ball, 
                        "uptime": self.text_cmd.uptime, "choice": self.text_cmd.choice, "coinflip": self.text_cmd.coinflip, "randomcase": self.text_cmd.randomcase,
                        "maximize": self.text_cmd.maximize, "reverse": self.text_cmd.reverse, "gift": self.text_cmd.gift, "dice": self.text_cmd.dice}



class COMMAND(BOT):
    def __init__(self, cmd, arguments, userid, msgid, msgchid, priv):
        super().__init__()
        self.command = cmd
        self.arguments = arguments
        self.user_id = userid
        self.message_id = msgid
        self.message_ch_id = msgchid
        self.is_priv = priv
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
            return "", 204
    

