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

    def plain(self):
        plain = ''
        for i, alert in enumerate(self.alert['alerts']):
            plain += '\n%s, %d/%d, %s, ' % (self.alert['status'].upper(), i + 1, len(self.alert['alerts']), alert['startsAt'])
            plain += '%s (%s, %s)' % (alert['annotations']['summary'], alert['labels']['customer'], alert['labels']['product'])
        return plain

    def html(self):
        html = ''
        for i, alert in enumerate(self.alert['alerts']):
            icon = ''; color = ''
            if self.alert['status'].upper() == 'RESOLVED':
                icon = ':)'; color = 'green'
            else:
                icon = ':\'('; color = 'red'
            html += '<br />%s <strong><span style="color:%s">%s %d/%d </span></strong>%s ' % (icon, color, self.alert['status'].upper(), i + 1, len(self.alert['alerts']), alert['startsAt'])
            html += '<strong>%s</strong> (%s, %s)' % (alert['annotations']['summary'], alert['labels']['customer'], alert['labels']['product'])
        return html

