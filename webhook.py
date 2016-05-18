#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request
from alert import PrometheusAlert
import posix_ipc as ipc
import json
import logging
import os
from common import load_config, QUEUE_ENCODING

LOG_FORMAT = os.path.basename(__file__) + ' %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

service = Flask(__name__)
conf = None


@service.route('/test', methods=['GET'])
def xmpp_test():
    global conf
    if not conf:
        conf = load_config()
    if not push_in_queue(construct_message(conf['xmpp_recipients'], 'test message for: %s' % conf['xmpp_recipients'])):
        return '', 500
    return '', 204


@service.route('/alert', methods=['POST'])
def prometheus_alert():
    global conf
    if not conf:
        conf = load_config()
    msg = PrometheusAlert(request.data.decode()).plain()
    html = PrometheusAlert(request.data.decode()).html()
    push_in_queue(construct_message(conf['xmpp_recipients'], msg, html))
    return '', 204


def construct_message(recipients, msg, html=None):
    if html:
        return json.dumps({'recipients': recipients, 'message': msg, 'html': html})
    return json.dumps({'recipients': recipients, 'message': msg})


def push_in_queue(msg):
    global conf
    try:
        queue = ipc.MessageQueue(name=conf['mq_name'])
        queue.send(msg.encode(encoding=QUEUE_ENCODING), timeout=0)
    except ipc.ExistentialError:
        queue.close()
        return False
    except ipc.BusyError:
        queue.close()
        return False
    return True


def main():
    global conf
    conf = load_config()
    service.run(host=conf['flask_host'], port=conf['flask_port'])


if __name__ == '__main__':
    main()
