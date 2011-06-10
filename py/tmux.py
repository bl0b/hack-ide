import os, sys

from base import *


def tmux(*args):
    cmd = 'tmux '+' '.join(args)
    #l = [x.strip() for x in os.popen('tmux '+cmd+' ; echo $?').xreadlines()]
    #return (cmd, l[:-1], int(l[-1]))
    print "TMUX>", cmd
    ret = (cmd, os.system(cmd))
    print ret[1]
    return ret

def tmux_window(cmd):
    return 'new-session -n %s -s %s "%s" \';\' detach'%(get_context_name(), get_context_name(), cmd)

def tmux_split(parent, opts, cmd):
    return 'split-window -d %s -t %s:%s.%i "%s"'%(opts, get_context_name(), get_context_name(), parent, cmd)

