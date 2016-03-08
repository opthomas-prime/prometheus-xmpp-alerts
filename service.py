#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request
from xmppbot import Bot
from alert import PrometheusAlert
from timeout import timeout
import json
import logging
import os

LOG_FORMAT = os.path.basename(__file__) + ' %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

XMPP_CONNECTED = False

service = Flask(__name__)

bot = None
conf = None

@service.route('/test', methods=['GET', 'POST'])
def xmpp_test():
    if not XMPP_CONNECTED:
        if not connect_xmpp():
            return ''
    bot.send_message_to('test', conf['xmpp_receivers'])
    return ''


@service.route('/alert', methods=['POST'])
def http_alert():
    if not XMPP_CONNECTED:
        if not connect_xmpp():
            return ''
    msg = PrometheusAlert(request.data.decode()).pretty()
    bot.send_message_to(msg, conf['xmpp_receivers'])
    return ''


def load_config():
    with open('conf.json') as f:
        return json.loads(''.join(f.readlines()))


def connect_xmpp():
    global bot, conf, XMPP_CONNECTED

    if not conf:
        conf = load_config()

    bot = Bot(conf['xmpp_jid'],
              conf['xmpp_password'])

    logging.info('attempting to connect to xmpp server...')
    bot.start(conf['xmpp_host'], conf['xmpp_port'])
    if not timeout(bot.start, [conf['xmpp_host'], conf['xmpp_port']], duration=5):
        logging.error('unable to connect to xmpp server.')
        return False

    XMPP_CONNECTED = True

    return True


def main():
    global bot, conf

    conf = load_config()

    service.run(host=conf['flask_host'],
                port=conf['flask_port'])


if __name__ == '__main__':
    main()
