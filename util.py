from datetime import datetime


__author__ = 'Ziga Vucko'


class Error(Exception):
    def __init__(self, message):
        super().__init__(message)

    def message(self):
        return self.args[0]


def current_time():
    return datetime.now()


def timestamp():
    return '[' + current_time().strftime('%Y-%m-%d %H:%M:%S') + ']'
