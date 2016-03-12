#!/usr/bin/env python
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
        pretty = ''
        for i, alert in enumerate(self.alert['alerts']):
            pretty += '\n*** %s ALERT %d/%d (%s) ***\n' % (self.alert['status'].upper(), i + 1, len(self.alert['alerts']), alert['startsAt'])
            for annotation in alert['annotations']:
                pretty += (alert['annotations'][annotation]) + '\n'
            labels = []
            for label in alert['labels']:
                labels.append('%s: %s' % (label, alert['labels'][label]))
            pretty += ', '.join(labels) + '\n'
        return pretty
