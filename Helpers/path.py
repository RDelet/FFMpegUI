# coding=ascii

"""
@!Brief
"""

import os

from Helpers.log import log


BIN_DIR = None
ICON = None
FFMPEG = None
FFPLAY = None
FFPROBE = None


def split(f):
    """
    !@Brief Split file path for get path, name and extension

    @type f: string
    @param f: File path to split

    @rtype: string, string, string
    @return: File path, File name, File extension
    """
    p, ne = os.path.split(f)
    n, e = os.path.splitext(ne)

    return os.path.normpath(p), n, e


def check_directory(p):
    """!@Brief If given directory path does not exists create it.

    @type p: str
    @param p: Directory Path.
    """
    if not os.path.isdir(p):
        log.error('Path "{0}" must be a dir !'.format(p))
    if not os.path.exists(p):
        os.makedirs(p)


def get_files(s_path):
    """
    !@Brief Get files in given directory.

    @type s_path: string
    @param s_path: Directory for get files.

    @rtype: list
    @return: List of files
    """
    files_path = []
    for s_file_name in os.listdir(s_path):
        object_path = os.path.normpath(os.path.join(s_path, s_file_name))
        if os.path.isfile(object_path):
            files_path.append(object_path)

    return files_path
