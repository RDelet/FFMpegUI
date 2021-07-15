# coding=ascii

"""
!@Brief UI logger
"""

import logging


class Handler(logging.Handler):

    __f = list()

    @classmethod
    def connect(cls, f):
        cls.__f.append(f)

    def emit(self, r):
        for f in self.__f:
            f('[{0}][{1}] {2}'.format(r.levelname, r.filename, r.msg) if log.level == logging.DEBUG else r.msg)

log = logging.getLogger('FFMPEG UI')
log.setLevel(logging.DEBUG)
log.addHandler(Handler())
