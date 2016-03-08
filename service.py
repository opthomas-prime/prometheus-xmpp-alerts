#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request
from xmppbot import Bot
from alert import PrometheusAlert
import json
import logging
import os
import sys

LOG_FORMAT = os.path.basename(__file__) + ' %(message)s'
LOG_LEVEL = logging.INFO

service = Flask(__name__)


@service.route('/test', methods=['GET', 'POST'])
def xmpp_test():
    bot.send_message_to('test', conf['xmpp_receivers'])
    return ''


@service.route('/alert', methods=['POST'])
def http_alert():
    msg = PrometheusAlert(request.data.decode()).pretty()
    bot.send_message_to(msg, conf['xmpp_receivers'])
    return ''


def load_config():
    with open('conf.json') as f:
        return json.loads(''.join(f.readlines()))


def main():
    global bot, conf

    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

    conf = load_config()

    bot = Bot(conf['xmpp_jid'],
              conf['xmpp_password'])

    if not bot.start(conf['xmpp_host'], conf['xmpp_port']):
        logging.error('unable to connect to xmpp server.')
        sys.exit(status=1)

    service.run(host=conf['flask_host'],
                port=conf['flask_port'])


if __name__ == '__main__':
    main()
