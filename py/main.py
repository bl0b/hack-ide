#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

from task import *
from hackide import *

script_name = sys.argv[0]
version = "0.1beta!"

def version():
    print script_name, "version", version, "© 2011 Damien 'bl0b' Leroux"

def about():
    print "invoke as follows:"
    print " %s ide-descr.hackide                to open this IDE"%script_name


def main(args):
    if "-h" in args or "--help" in args or "help" in args:
        about()
        return 0
    if len(args)==1:
        tmuxrcdir = '/'.join(sys.path[0].split('/')[:-1])
        taskdefdir = tmuxrcdir+'/tasks'
        tmuxrc = rc_file('tmuxrc', open(tmuxrcdir+'/default.tmuxrc').read()).path
        for task_def in os.listdir(taskdefdir):
            if not task_def.endswith('.task'):
                continue
            print "importing task template", task_def
            create_task_class(taskdefdir+'/'+task_def)
        hi = read_hackide(args[0])
        defensive_layout = reduce(lambda a, b: a+[b, 'has-session -t '+get_context_name()], hi['layout'], [])[:-1]
        all_cmds = filter(lambda x: x, (l.strip() for l in open(tmuxrc).xreadlines())) + defensive_layout + [ 'attach -t '+get_context_name() ]
        ret = [ tmux(c) for c in all_cmds ]
    return 0





if __name__=='__main__':
    sys.exit(main(sys.argv[1:]))
