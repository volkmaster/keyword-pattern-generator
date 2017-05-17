from datetime import datetime


__author__ = 'Ziga Vucko'


def current_time():
    return datetime.now()


def timestamp():
    return '[' + current_time().strftime('%Y-%m-%d %H:%M:%S') + ']'
