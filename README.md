# prometheus-xmpp-alerts
XMPP-Bot with HTTP-API for Monitoring Alerts

## Dependencies
- sudo pip3 install flask
- sudo pip3 install gunicorn
- sudo pip3 install sleekxmpp

## Start
- python3 prometheus-xmpp-alerts.py
- gunicorn -w 5 -b 0.0.0.0:8080 prometheus-xmpp-alerts:app