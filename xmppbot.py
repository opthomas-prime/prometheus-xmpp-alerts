#!/usr/bin/env python3
# -*- coding: utf-8 -*-import sys

import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout

class Bot(ClientXMPP):
    def __init__(self, jid, password, host, port):
        ClientXMPP.__init__(self, jid=jid, password=password)
        self.add_event_handler('session_start', self.session_start)
        self.add_event_handler('message', self.message)

        logging.basicConfig(level=logging.DEBUG , format='[sleekxmpp] %(message)s')
        self.connect((host, port))
        self.process()

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            self.send_message(mto=msg['from'], mbody='Thanks for sending:\n%s' % msg['body'])