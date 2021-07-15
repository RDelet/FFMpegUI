# coding=ascii

"""
@!Brief
"""

import logging
import os
import traceback

from PySide2 import QtCore

from Helpers import path, process
from Helpers.ffmpeg import FFMPEG


class Thread(QtCore.QThread):

    log = QtCore.Signal(str, int)

    def __init__(self, d, parent=None):
        super(Thread, self).__init__(parent)
        self.data = d

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '{0}'.format(self.__class__.__name__)

    def __build_command(self):
        """!@Brief Create ffmpeg command
                   ToDo: Add convert from images
                         ...
                   ToDo: Add convert to image
                         ffmpeg -i "path.mp4" -vf "select='eq(pict_type,PICT_TYPE_I)'" -vsync vfr "path%04d.tga"
                   ToDo: add video quality option -q:v 2
                         -y --> overide output
                         -n --> never overide output
                         -map 0:v --> Toutes les pistes videos
                         -map 0:a --> Toutes les pistes audios

        @rtype: str
        @return: Command.
        """
        cmd = '{0} -n -i "{1}" -map 0:v -map 0:a -c:a aac -c:v "{2}" -preset {3} -crf {4}'.format(FFMPEG.get_app(),
                                                                                                  self.data.file_path,
                                                                                                  self.data.video_codec,
                                                                                                  self.data.preset,
                                                                                                  self.data.crf)
        if self.data.size is not None:
            cmd += ' -s {0}'.format(self.data.size)
        cmd += ' "{0}"'.format(self.data.output_path)

        return cmd

    def run(self):
        path.check_directory(self.data.output_dir)
        if os.path.exists(self.data.output_path):
            print('File "{0}" already exist !'.format(self.data.full_name))
            return
        try:
            cmd = self.__build_command()
            self.log.emit(cmd, logging.DEBUG)
            proc = process.popen(cmd)
            for line in process.unbuffered(proc):
                self.log.emit(line, logging.INFO)
        except Exception as e:
            self.log.emit(traceback.format_exc(e), logging.ERROR)
