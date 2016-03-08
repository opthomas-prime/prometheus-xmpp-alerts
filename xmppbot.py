#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sleekxmpp import ClientXMPP
import json
import logging
import os
import posix_ipc as ipc
import sys
import signal
from timeout import timeout

LOG_FORMAT = os.path.basename(__file__) + ' %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

queue = None


class Bot(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid=jid, password=password)
        self.add_event_handler('session_start', self.session_start_handler)

    def start(self, host, port):
        if not self.connect((host, port), reattempt=True):
            return False
        self.process()
        return True

    def session_start_handler(self, _):
        self.send_presence()
        self.get_roster()

    def send_message_to(self, msg, receivers):
        for receiver in receivers:
            self.send_message(mto=receiver, mbody=msg)


def load_config():
    with open('conf.json') as f:
        return json.loads(''.join(f.readlines()))


def terminate(sig, _):
    global queue

    if queue:
        try:
            queue.close()
            queue.unlink()
        except ipc.ExistentialError:
            pass
    sys.exit(1)


def main():
    global queue

    conf = load_config()

    bot = Bot(conf['xmpp_jid'], conf['xmpp_password'])
    if not timeout(bot.start, [conf['xmpp_host'], conf['xmpp_port']], duration=5):
        logging.error('unable to connect to xmpp server.')
        terminate()

    queue = ipc.MessageQueue(name=conf['mq_name'], flags=ipc.O_CREAT)
    while True:
        try:
            queue.receive(0)
        except ipc.BusyError:
            break

    signal.signal(signal.SIGINT, terminate)
    try:
        while True:
            bot.send_message_to(queue.receive()[0].decode(encoding='utf-8'), conf['xmpp_receivers'])
    except KeyboardInterrupt:
        terminate(None, None)
    except ipc.SignalError:
        terminate(None, None)


if __name__ == '__main__':
    main()
