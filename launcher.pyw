# coding=ascii

"""
@!Brief
"""

if __name__ == '__main__':

    import os
    import sys

    CURRENT_PATH = os.path.dirname(sys.argv[0])
    TOOL_DIR = os.path.split(CURRENT_PATH)[0]
    if TOOL_DIR not in sys.path:
        sys.path.insert(0, TOOL_DIR)

    from Helpers import path

    path.BIN_DIR = os.path.normpath(os.path.join(CURRENT_PATH, "bin"))
    path.ICON = os.path.normpath(os.path.join(CURRENT_PATH, "icons"))
    path.FFMPEG = os.path.normpath(os.path.join(path.BIN_DIR, "ffmpeg"))
    path.FFPROBE = os.path.normpath(os.path.join(path.BIN_DIR, "ffprobe"))
    path.FFPLAY = os.path.normpath(os.path.join(path.BIN_DIR, "ffplay"))

    from UI import ui
    ui.main()
