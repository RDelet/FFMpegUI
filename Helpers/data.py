# coding=ascii

"""
@!Brief
"""

import os

from PySide2 import QtCore

from Helpers import path
from Helpers.log import log


DATA_ROLE = QtCore.Qt.UserRole


class Item(object):

    """
    @!Brief
    """

    def __init__(self, f):

        self.file_path = f
        self.path, self._name, e = path.split(f)
        self.extension = e.split(".")[-1]
        self.output_dir = os.path.join(self.path, 'Converted')
        self.output_extension = "mp4"
        self.video_codec = "libx265"
        self.audio_codec = None
        self.preset = "medium"
        self.crf = 28
        self.size = None  # 1920*1080
        self.use_suffix = True

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.name)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, v):
        old = self._name
        self._name = v.split('.')[0]
        log.info('Name {0} change to {1}'.format(old, self._name))

    @property
    def full_name(self):
        """!@Brief Get full file name.
                   If file already exists add codec as suffix.

        @rtype: str
        @return: Value.
        """
        f = '{0}.{1}'.format(self.name, self.output_extension)
        if os.path.exists(os.path.join(self.output_dir, f)):
            f = '{0}_{1}.{2}'.format(self.name, self.video_codec, self.output_extension)
        if os.path.exists(os.path.join(self.output_dir, f)):
            log.error('Path "{0}" already exists !'.format(f))
            return

        return f

    @property
    def output_path(self):
        return os.path.join(self.output_dir, self.full_name)


class Codec(object):

    def __init__(self, s_name, s_description):
        self.name = s_name
        self.description = s_description

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.name)
