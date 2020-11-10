import flask
from flask import Flask, request, jsonify, Response, abort
import commands
import json
import sys
import os

class TEXT:
    def __init__(self):
        super().__init__()
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
