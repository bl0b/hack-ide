import startup

import os, sys, re

from tmux import *
from task import *
from layout import *
from hackide import *


#class vim_task(task):
#    rc_contents = """source /etc/vim/vimrc
#source ~/.vimrc
#let g:session_autosave = 'no'
#let g:session_directory = '%s'
#map <F8> <Esc>:SaveSession %%T%%
#map <F5> <Esc>:OpenSession %%T%%
#"""%ide_data_path
#    def __init__(self, contextname, taskname, param):
#        task.__init__(self, contextname, taskname, param)
#        self['VIMINFO'] = rc_file(taskname+'.viminfo').path
#        self['VIMSESSION'] = rc_file(taskname+'.vim').path
#        self['VIMRC'] = rc_file(taskname+'.vimrc', self.parse(vim_task.rc_contents)).path
#        self.cmd_template = "vim -u %VIMRC% -i %VIMINFO% -S %VIMSESSION%"
#        self.cmd_wd = "."
#
#class cmd_task(task):
#    def __init__(self, contextname, taskname, param):
#        task.__init__(self, contextname, taskname, param)
#        words = param.split(' ')
#        self.cmd_wd = words[0]
#        self.cmd_template = ' '.join(words[1:])
#
#class interactive_shell_task(task):
#    def __init__(self, contextname, taskname, param):
#        task.__init__(self, contextname, taskname, param)
#        self['HF'] = rc_file(taskname+'.bash_history').path
#        self.cmd_template = "HISTFILE=%HF% bash -i"
#        self.cmd_wd = param or '.'
#



if __name__=='__main__':
    tmuxrc = rc_file("tmuxrc", open(sys.path[0]+'/../default.tmuxrc').read()).path
    taskdefdir = '/'.join(sys.path[0].split('/')[:-1]+['tasks'])
    for task_def in os.listdir(taskdefdir):
        if not task_def.endswith('.task'):
            continue
        print "importing task template", task_def
        create_task_class(taskdefdir+'/'+task_def)
    #print task_registry
    hi = read_hackide(sys.path[0]+'/../sample.hackide')
    #print all_tasks.keys()
    #print all_rc.keys()
    #layout.set_index()
    #cmds = [ 'new-session -d -s %s -n hack-ide'%get_context_name() ] + layout.tmux_cmds() + [ 'attach-session -t '+get_context_name() ]
    #cmdbuf = '-f %s '%tmuxrc + " ';' ".join(cmds)
    #tmux(cmdbuf)
    #print cmdbuf
    #tmux(cmdbuf)
    #print layout.flat_pane_list()
    all_cmds = filter(lambda x: x, (l.strip() for l in open(tmuxrc).xreadlines())) + hi['layout'] + [ 'attach -t '+get_context_name() ]
    cmdbuf = " ';' ".join(all_cmds)
    print hi
    print
    print '\n'.join(all_cmds)

