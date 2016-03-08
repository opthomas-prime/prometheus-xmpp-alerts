#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal

DEFAULT_TIMEOUT_SEC = 1


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
