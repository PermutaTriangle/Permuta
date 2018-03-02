import math
import sys
import time


class ProgressBar(object):

    @staticmethod
    def create(mx, mn=0):
        ProgressBar.mn = mn
        ProgressBar.mx = mx
        ProgressBar.at = mn
        ProgressBar.start = time.time()
        ProgressBar.last = 0
        ProgressBar.curw = 0
        # sys.stderr.write('\n')
        ProgressBar.progress(mn)

    @staticmethod
    def clear():
        sys.stderr.write('\r')
        sys.stderr.write(' ' * ProgressBar.curw)
        sys.stderr.write('\r')

    @staticmethod
    def draw(fin=False):
        # sys.stderr.write('\033[1F')
        sys.stderr.write('\r')
        width = 50
        prog = (1 if ProgressBar.mn == ProgressBar.mx
                else (float(ProgressBar.at - ProgressBar.mn) /
                      (ProgressBar.mx - ProgressBar.mn)))
        bars = int(round(prog * width))
        bars = max(0, min(width, bars))
        here = '%3d%% [%s%s] ' % (
            round(prog * 100), '#' * bars, '-' * (width - bars))
        ProgressBar.curw = len(here)
        sys.stderr.write(here)
        elapsed = ProgressBar.last - ProgressBar.start
        # if elapsed >= 4 and prog > 0:
        show_time = None
        if fin:
            show_time = elapsed
        elif elapsed >= 2 and prog > 0:
            show_time = max(0, elapsed / prog - elapsed)
        if show_time is not None:
            h = math.floor(show_time / 60 / 60)
            show_time -= h * 60 * 60
            m = math.floor(show_time / 60)
            show_time -= m * 60
            s = math.floor(show_time)
            here = ' %02d:%02d:%02d' % (h, m, s)
            sys.stderr.write(here)
            ProgressBar.curw += len(here)
        # sys.stderr.write('\n')

    @staticmethod
    def progress(prg=None, fin=False):
        if prg is not None:
            ProgressBar.at = prg
        else:
            ProgressBar.at = ProgressBar.at + 1
            prg = ProgressBar.at
        curt = time.time()
        if curt - ProgressBar.last < 0.5 and not fin:
            return
        ProgressBar.last = curt
        ProgressBar.draw(fin)

    @staticmethod
    def finish():
        ProgressBar.progress(ProgressBar.mx, fin=True)
        sys.stderr.write('\n')
