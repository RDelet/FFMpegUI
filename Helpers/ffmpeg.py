# coding=ascii

"""
@!Brief
"""

import os
import subprocess

from Helpers import path


class FFMPEG(object):

    # =========================================================
    #    Enum
    # =========================================================

    class AppName(object):

        kFFMpeg = "ffmpeg"
        kFFPlay = "ffplay"
        kFFProbe = "ffprobe"

    class BaseCommand(object):

        kFormats = "-formats"
        kEncoders = "-encoders"

    def __init__(self, label):
        self.label = label

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.label)

    @staticmethod
    def get_app(app=AppName.kFFMpeg):
        return os.path.normpath(os.path.join(path.BIN_DIR, app))

    def get_video_codecs(self, **kwargs):

        """
        !@Brief Get codecs of ffmpeg.
        """

        codec_types = self.codec_types(**kwargs)
        cmd = "{exe} {args}".format(exe=self.get_app(), args=self.BaseCommand.kEncoders)
        proc = subprocess.check_output(
            cmd,
            shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
            bufsize=1, universal_newlines=True
        )

        proc_split = proc.split("\n")
        codec_start = proc_split.index(' ------')

        codecs = {}
        for p_split in proc_split[codec_start + 1:]:

            splits = p_split.split(" ")

            if not splits:
                continue
            if len(splits) == 1:
                continue
            if [x for x in codec_types if x not in splits[1]]:
                continue

            description = ""
            for split in splits[3:]:
                if split != "":
                    description += "%s " % split

            codecs[splits[2]] = description

        return codecs

    @staticmethod
    def video_containers():
        """
        !@Brief Get all containers.
        """
        return ["mp4", "avi", "mov", "flv", "webm", "mkv", "flv", "vob", "ogv", "ogg", "drc", "gif", "gifv",
                "mng", "qt", "wmv", "yuv", "rm", "rmvb", "asf", "amv", "m4p", "m4v", "mpg", "mp2", "mpeg",
                "mpe", "mpv", "m2v", "m4v", "svi", "3gp", "3g2", "mxf", "roq", "nsv", "f4v", "f4p", "f4a",
                "f4b"]

    @staticmethod
    def video_preset():
        return ["placebo", "veryslow", "slower", "slow", "medium", "fast", "faster", "veryfast", "superfast",
                "ultrafast"]

    @staticmethod
    def codec_types(**kwargs):
        """
        !@Brief Get all codecs types.
        """
        codec_types = list()
        if kwargs.get("decode", False):
            codec_types.append("D")
        if kwargs.get("encode", False):
            codec_types.append("E")
        if kwargs.get("video", False):
            codec_types.append("V")
        if kwargs.get("audio", False):
            codec_types.append("A")
        if kwargs.get("subtitle", False):
            codec_types.append("S")

        return codec_types
