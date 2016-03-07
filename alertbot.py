#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from xmppbot import Bot
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

def load_config():
    with open('conf.json') as f:
        return json.loads(''.join(f.readlines()))

if __name__ == '__main__':
    conf = load_config()

    bot = Bot(conf['jid'], conf['password'], conf['host'], conf['port'])


    app.run(host='0.0.0.0', port=8080)
