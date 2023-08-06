# This file is in the Public Domain.

from run import getmain

def cmd(event):
    tbl = getmain("tbl")
    event.reply(",".join(sorted(tbl.modnames)))
