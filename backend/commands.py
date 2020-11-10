import time
import sys
import math
import text_cmd



class BOT:
    def __init__(self):
        self.text_cmd = text_cmd.TEXT()
        self.start_time = time.time()
        self.LOOK_UP = {"ping": self.text_cmd.ping, "pong": self.text_cmd.pong, "repeat": self.text_cmd.repeat}

    def getUptime(self):
        return time.time() - self.start_time

class COMMAND(BOT):
    def __init__(self, cmd, arguments):
        super().__init__()
        self.command = cmd
        self.arguments = arguments

    def lookup(self):
        if self.LOOK_UP[self.command]:
            return True
        else:
            return False

    def execute(self):
        if self.lookup():
            return self.LOOK_UP[self.command](self.arguments)
        else:
            return "", 204

    # def pong(self):
    #     return self.LOOK_UP["pong"](self.arguments)
    
    # def repeat(self):
    #     return self.LOOK_UP["repeat"](self.arguments)

    

