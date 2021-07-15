# coding=ascii

"""
!@Brief Maya process helpers.
"""

import contextlib
import subprocess


def popen(cmd):
    """!@Brief Create python subProcess.Popen

    @rtype: subprocess.Popen
    @return: Process
    """
    return subprocess.Popen(cmd, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            bufsize=1, universal_newlines=True, shell=True)


def unbuffered(proc, s_stream='stdout'):
    """
    !@Brief Get subprocess log and print in realtime.

    @type proc: subprocess.Popen
    @param proc: Subprocess.
    @type s_stream: string
    @param s_stream: Type of variable you want to parse in subprocess.

    @rtype: string
    @return: Current log returned by subprocess.
    """
    stream = getattr(proc, s_stream)
    with contextlib.closing(stream):
        while True:
            out = []
            last = stream.read(1)
            # Don't loop forever
            if last == '' and proc.poll() is not None:
                break
            while last not in ['\n', '\r\n', '\r']:
                # Don't loop forever
                if last == '' and proc.poll() is not None:
                    break
                out.append(last)
                last = stream.read(1)
            out = ''.join(out)
            yield out
