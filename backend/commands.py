import time
import sys
import math
import text_cmd

class BOT:
    def __init__(self):
        self.text_cmd = text_cmd.TEXT()
        self.start_time = time.time()
        self.command_list = ["ping", "pong", "repeat"]

    def getUptime(self):
        return time.time() - self.start_time

class COMMAND(BOT):
    def __init__(self, cmd):
        super().__init__()
        self.command = cmd

    def lookup(self):
        if self.command in self.command_list:
            return True
        else:
            return False

    def pong(self):
        return self.text_cmd.pong()

    

