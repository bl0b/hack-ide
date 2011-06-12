import os, sys

from base import *

__all__ = [ 'tmux', 'tmux_split', 'tmux_window' ]

app_name = 'hack-ide'

def tmux(*args):
    cmd = ' '.join(args)
    #l = [x.strip() for x in os.popen('tmux '+cmd+' ; echo $?').xreadlines()]
    #return (cmd, l[:-1], int(l[-1]))
    print "TMUX>", repr(cmd)
    ret = (cmd, os.system('tmux '+cmd))
    print ret[1]
    if ret[1]!=0:
        raise ValueError(cmd)
    return ret

def tmux_window(cmd):
    #return 'new-session -n %s -s %s "%s" \';\' detach'%(app_name, get_context_name(), cmd)
    return 'new-session -d -n %s -s %s "%s"'%(app_name, get_context_name(), cmd)

def tmux_split(parent, opts, cmd):
    return 'split-window %s -t %s:%s.%i "%s"'%(opts, get_context_name(), app_name, parent, cmd)

