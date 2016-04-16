# prometheus-xmpp-alerts
XMPP-Bot with Webhook for Monitoring Alerts from Prometheus (https://prometheus.io/docs/alerting/alertmanager/).

Prometheus's Alertmanager doesn't support alerting via XMPP/Jabber messages at the moment. Since i want to receive alters on my mobile devices and i like XMPP, i built this tool.

If you want to use this tool but the description to configure/run it is not sufficient, feel free to contact me.

## How it works

```
|
| Alertmanager (Webhook receiver)
|
|             +------------+
+------------>| webhook.py |---+
              +------------+   |
                               |
                               | POSIX IPC MQ
                               |
              +------------+   |
+-------------| xmppbot.py |<--+
|             +------------+
|
| XMPP Messages
|
```

### webhook.py
Receives the Alerts from Promtheus via Webhook and pushes them into a POSIX IPC MQ.

#### Start
- For testing purposes you can start this script with python. Simply call: `python webhook.py`
- For 'production use' start the flask app with gunicorn: `gunicorn -w 5 -b 0.0.0.0:8080 webhook:service`

### xmppbot.py
Pulls the Alerts from the POSIX IPC MQ and sends them to the configured XMPP recipients.

#### Start
- Start the XMPP bot with: `python xmppbot.py`

## Configuration
- Both components can be configured in the configuration file `conf.json`

## Dependencies (Package names for Debian)
- `pip install flask`
- `pip install gunicorn`
- `pip install sleekxmpp`
- `apt-get install build-essential python-dev`
- `pip install posix_ipc`

## Run in 'production'
- Tip: I use `supervisord` to run that kind of script automatically at boot.

