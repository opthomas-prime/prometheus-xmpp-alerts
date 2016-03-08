#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sleekxmpp import ClientXMPP
import logging

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
        logging.info('sending following message to: %s' % ','.join(receivers))
        logging.info(msg)
        for receiver in receivers:
            self.send_message(mto=receiver, mbody=msg)
