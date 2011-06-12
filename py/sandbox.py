import startup

import os, sys, re

from tmux import *
from task import *
from layout import *
from hackide import *




if __name__=='__main__':
    os.unsetenv('TMUX')
    sys.argv+=['hackide']
    from main import respawn
    tmuxrc = rc_file("tmuxrc", open(sys.path[0]+'/../default.tmuxrc').read()).path
    taskdefdir = '/'.join(sys.path[0].split('/')[:-1]+['tasks'])
    for task_def in os.listdir(taskdefdir):
        if not task_def.endswith('.task'):
            continue
        print "importing task template", task_def
        create_task_class(taskdefdir+'/'+task_def)
    #print task_registry
    #hi = read_hackide(sys.path[0]+'/../sample.hackide')
    #print all_tasks.keys()
    #print all_rc.keys()
    #layout.set_index()
    #cmds = [ 'new-session -d -s %s -n hack-ide'%get_context_name() ] + layout.tmux_cmds() + [ 'attach-session -t '+get_context_name() ]
    #cmdbuf = '-f %s '%tmuxrc + " ';' ".join(cmds)
    #tmux(cmdbuf)
    #print cmdbuf
    #tmux(cmdbuf)
    #print layout.flat_pane_list()
    #all_cmds = filter(lambda x: x, (l.strip() for l in open(tmuxrc).xreadlines())) + hi['layout'] + [ 'attach -t '+get_context_name() ]
    #cmdbuf = " ';' ".join(all_cmds)
    #print hi
    #print
    #print '\n'.join(all_cmds)
    hi = read_hackide('../test/gros.hackide')

