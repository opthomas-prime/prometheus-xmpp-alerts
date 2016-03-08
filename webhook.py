#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request
from alert import PrometheusAlert
import posix_ipc as ipc
import json
import logging
import os

LOG_FORMAT = os.path.basename(__file__) + ' %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

service = Flask(__name__)


@service.route('/test', methods=['GET', 'POST'])
def xmpp_test():
    if not push_in_queue('just a test'.encode(encoding='utf-8')):
        return 'failed to push in queue'
    return 'success'


@service.route('/alert', methods=['POST'])
def http_alert():
    msg = PrometheusAlert(request.data.decode()).pretty()
    push_in_queue(msg.encode(encoding='utf-8'))
    return ''


def push_in_queue(msg):
    conf = load_config()
    try:
        queue = ipc.MessageQueue(name=conf['mq_name'])
        queue.send(msg, timeout=0)
    except ipc.ExistentialError:
        return False
    except ipc.BusyError:
        return False
    finally:
        queue.close()
    return True


def load_config():
    with open('conf.json') as f:
        return json.loads(''.join(f.readlines()))


def main():
    conf = load_config()

    service.run(host=conf['flask_host'],
                port=conf['flask_port'])


if __name__ == '__main__':
    main()
