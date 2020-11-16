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
        
    def pong(self, arguments):
        return {"response":"Ping!"}
    
    def ping(self, arguments):
        return {"response":"Pong!"}
    
    def repeat(self, arguments):
        response = {
            "response": "Specify something for me to repeat!"
        }
        if len(arguments) > 0:
            response["response"] = " ".join(arguments)
        return jsonify(response)

    def eight_ball(self, arguments):
        responses = ["As I see it, yes.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.", "Yes.", "Yes – definitely.", "You may rely on it."]
        if not arguments:
            return {"response": "Nothing to provide a value to...."}
        resp = random.randint(0, len(responses))
        response = {"response": responses[resp]}
        return jsonify(response)

    def uptime(self, arguments=None):
        delta = datetime.datetime.now() - start_time
        days = delta.days
        hours, seconds = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        duration = "{0} days, {1} hours, {2} minutes, and {3} seconds".format(days, hours, minutes, seconds)
        return {"response": duration}