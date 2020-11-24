import flask
from flask import Flask, request, jsonify, Response, abort
import commands
import json
import sys
import random
from backend import *
import datetime
import os

class TEXT:
    def __init__(self):
        pass
        
    def pong(self, arguments, pack):
        val = {"response":"Ping!"}
        return jsonify(val)
    
    def ping(self, arguments, pack):
        val = {"response":"Pong!"}
        return jsonify(val)
    
    def repeat(self, arguments, pack):
        response = {
            "response": "Specify something for me to repeat!"
        }
        if len(arguments) > 0:
            response["response"] = " ".join(arguments)
        return jsonify(response)

    def eight_ball(self, arguments, pack):
        responses = ["As I see it, yes.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.", "Yes.", "Yes – definitely.", "You may rely on it."]
        if not arguments:
            return {"response": "Nothing to provide a value to...."}
        resp = random.randint(0, len(responses)-1)
        response = {"response": responses[resp]}
        return jsonify(response)

    def uptime(self, arguments=None, pack=None):
        delta = datetime.datetime.now() - start_time
        days = delta.days
        hours, seconds = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        duration = "{0} days, {1} hours, {2} minutes, and {3} seconds".format(days, hours, minutes, seconds)
        return {"response": duration}

    def choice(self, arguments, pack):
        if not arguments:
            return {"response": "No arguments supplied."}
        resp = random.randint(0, len(arguments)-1)
        return {"response": "<@{0}> {1}".format(pack["user_id"],arguments[resp])}

    def coinflip(self, arguments=None, pack=None):
        user_id = pack["user_id"]
        val = random.randint(0, 100)
        if 0 <= val < 50:
            return {"response": "<@{0}> Heads".format(user_id)}
        else:
            return {"response": "<@{0}> Tails".format(user_id)}
    
    def randomcase(self, arguments, pack):
        if not arguments:
            return {"response": "Nothing for me to case :("}
        
        val = ""
        
        for i in arguments:
            val += i
            val += " "
        val.strip()

        funs = [0, 1]
        retstr = ""

        for v,i in enumerate(val):
            if i.isalpha():
                choice = random.choice(funs)
                if choice:
                    retstr += i.upper()
                else:
                    retstr += i.lower()
            else:
                retstr += i
        return {"response": retstr}
    
    def maximize(self, arguments, pack):
        if not arguments:
            return {"response": "Nothing to maximize."}
        originalarg = arguments[0]
        for i in arguments:
            originalarg += i
            originalarg += " "

        valstr = originalarg
        while len(valstr) <= (2000 - len(originalarg)):
            valstr += originalarg
            valstr += " "
        if len(valstr) < 2000:
            difference = 2000 - len(valstr)
            valstr += originalarg[0:difference]
        return {"response": valstr}
    
    def reverse(self, arguments, pack):
        if not arguments:
            return {"response": "Nothing to reverse."}
        v = ""
        for i in arguments:
            v += i
            v += " "
        revers = v[::-1]
        return {"response": revers}

    def gift(self, arguments, pack):
        if not arguments:
            return {"response": "Nobody to gift."}
        user_id = arguments[0]

        length = len(arguments)
        choices = arguments[1:]
        res = random.choice(choices)

        return {"response": "{0}, you just received a gift: a {1}".format(user_id, res)}
 
    def dice(self, arguments, pack):
        if not arguments:
            return {"response": "No number passed."}
        num_dice = arguments[0]
        
        