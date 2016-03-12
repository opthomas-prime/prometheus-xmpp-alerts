#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import signal

QUEUE_ENCODING = 'utf-8'

DEFAULT_TIMEOUT_SEC = 5

def timeout(func, args=(), kwargs={}, duration=DEFAULT_TIMEOUT_SEC):
    class FunctionTimeoutError(Exception):
        pass

    def handler(sig, _):
        raise FunctionTimeoutError()

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(duration)
    try:
        result = func(*args, **kwargs)
    except FunctionTimeoutError:
        result = None
    finally:
        signal.alarm(0)
    return result


def load_config():
    with open('conf.json') as f:
        return json.loads(''.join(f.readlines()))
