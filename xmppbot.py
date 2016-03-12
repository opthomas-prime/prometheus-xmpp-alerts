#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sleekxmpp import ClientXMPP
import json
import logging
import os
import posix_ipc as ipc
import sys
from common import timeout, load_config, QUEUE_ENCODING

LOG_FORMAT = os.path.basename(__file__) + ' %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


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


class IPCReceiver:
    def __init__(self, mq_name):
        self.queue = ipc.MessageQueue(name=mq_name, flags=ipc.O_CREAT)
        while True:
            try:
                self.queue.receive(0)
            except ipc.BusyError:
                break

    def cleanup(self):
        if self.queue:
            try:
                self.queue.close()
                self.queue.unlink()
            except ipc.ExistentialError:
                pass

    def receive(self):
        return self.queue.receive()[0].decode(QUEUE_ENCODING)


def main():
    conf = load_config()
    bot = Bot(conf['xmpp_jid'], conf['xmpp_password'])
    if not timeout(bot.start, [conf['xmpp_host'], conf['xmpp_port']]):
        terminate()
    receiver = IPCReceiver(conf['mq_name'])
    try:
        while True:
            data = json.loads(receiver.receive())
            bot.send_message_to(data['message'], data['recipients'])
    except KeyboardInterrupt:
        pass
    except ipc.SignalError:
        pass
    finally:
        receiver.cleanup()
        terminate()


def terminate():
    sys.exit(1)


if __name__ == '__main__':
    main()
