#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


# {
#  "version": "2",
#  "status": "<resolved|firing>",
#  "alerts": [
#    {
#      "labels": <object>,
#      "annotations": <object>,
#      "startsAt": "<rfc3339>",
#      "endsAt": "<rfc3339>"
#    },
#    ...
#  ]
# }

class PrometheusAlert:
    def __init__(self, alert):
        self.alert = json.loads(alert)

    def pretty(self):
        pretty = '**** %s ****\n' % self.alert['status']
        for i, alert in enumerate(self.alert['alerts']):
            pretty += '**** alert %d/%d ****\n' % (i + 1, len(self.alert['alerts']))
            pretty += '* annotations *\n'
            for annotation in alert['annotations']:
                pretty += '%s: %s\n' % (annotation, alert['annotations'][annotation])
            pretty += '* labels *\n'
            for label in alert['labels']:
                pretty += '%s: %s\n' % (label, alert['labels'][label])
            pretty += '* time *\n'
            pretty += 'startsAt: %s\n' % alert['startsAt']
            pretty += 'endsAt: %s\n' % alert['endsAt']
        return pretty
