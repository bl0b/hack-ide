import os, sys

from base import *
from rc_file import rc_file

__all__ = [ 'tmux', 'tmux_split', 'tmux_window', 'tmux_query', 'tmuxrc' ]

app_name = 'hack-ide'

tmuxrc = rc_file("tmuxrc", open(sys.path[0]+'/../default.tmuxrc').read()).path

import subprocess
import shlex

# cf https://bugs.launchpad.net/ubuntu/+source/tmux/+bug/771581
tmux_popen_blacklist = set(['new-session', 'new-window', 'split-window'])

def tmux(args):
    cmd = ['tmux']+(type(args) is str and shlex.split(args) or list(args))
    if tmux_popen_blacklist.intersection(cmd):
        print "ignoring i/o for", cmd
        #return (cmd, os.system(' '.join(cmd)), '')
        return (cmd, subprocess.Popen(cmd).wait(), '', '')
    try:
        print cmd, '=>',
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = p.communicate()
        print repr(out)
        return (cmd, p.returncode, out, err)
    except subprocess.CalledProcessError, cpe:
        ret = (cmd, cpe.returncode, cpe.output, 'n/a')
        print "TMUX FAILURE", ret
        return ret

def tmux_window(cmd, name=app_name):
    return 'new-session -d -n %s -s %s "%s"'%(app_name, get_context_name(), cmd)

def tmux_split(parent, opts, cmd, name=app_name):
    return 'split-window %s -t %s:%s.%i "%s"'%(opts, get_context_name(), app_name, parent, cmd)

def tmux_query(*what):
    return tmux(what)

