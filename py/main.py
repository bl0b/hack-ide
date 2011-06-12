#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

from base import *
from tmux import *
from task import *
from hackide import *
from layout import *

script_name = len(sys.argv)>1 and sys.argv[1] or sys.argv[0]
script_version = "0.1beta!"

def version():
    print script_name, "version", script_version, "© 2011 Damien 'bl0b' Leroux"
    print

def about():
    version()
    print "invoke as follows:"
    print " %s ide-descr.hackide                to open this IDE"%script_name
    print " %s files ide-descr.hackide          to list the resource files used by this IDE"%script_name
    print " %s templates                        to list the available task templates"%script_name

def respawn(hi, tmuxrc):
    print 'DEBUG', hi
    print 'DEBUG', hi['layout']
    rc = '-f %s '%tmuxrc
    ret = []
    try:
        session_exists = tmux('has-session -t '+hi['context'])[1]==0
    except ValueError, ve:
        session_exists = False
    if session_exists:
        print "[Reattaching to existing session %s]"%hi['context']
        try:
            ret = [ tmux('-f %s attach -t %s'%(tmuxrc, hi['context'])) ]
        except ValueError, ve:
            print "An error occurred while sending command", ve.message
            return []
    else:
        print "[Spawning new session %s]"%hi['context']
        lcmd = layout2tmux()

        defensive_layout = lcmd[:1] # don't check for session before the new-session :)
        defensive_layout += map(lambda b: 'has-session -t '+get_context_name()+" ';' "+b, lcmd[1:])

        all_cmds = [ '-f %s start-server'%tmuxrc ]
        all_cmds += defensive_layout
        all_cmds += [ '-f %s attach -t %s'%(tmuxrc, get_context_name()) ]

        try:
            ret = [ tmux(c) for c in all_cmds ]
        except ValueError, ve:
            print "An error occurred while creating session"
            print ve
            return []

    return ret


def main(args):
    tmuxrcdir = '/'.join(sys.path[0].split('/')[:-1])
    tmuxrc = rc_file('tmuxrc', open(tmuxrcdir+'/default.tmuxrc').read()).path
    taskdefdir = tmuxrcdir+'/tasks'
    for task_def in os.listdir(taskdefdir):
        if not task_def.endswith('.task'):
            continue
        #print "importing task template", task_def
        create_task_class(taskdefdir+'/'+task_def)
    taskdefdir = tmuxrcdir+'/tasks'
    for task_def in os.listdir(taskdefdir):
        if not task_def.endswith('.task'):
            continue
        #print "importing task template", task_def
        create_task_class(taskdefdir+'/'+task_def)
    if len(args)==0 or "-h" in args or "--help" in args or "help" in args:
        about()
        return 0
    if "-V" in args or "--version" in args or "version" in args:
        version()
        return 0
    if len(args)==1:
        if os.path.isfile(args[0]):
            respawn(read_hackide(open(args[0]).xreadlines()), tmuxrc)
        elif args[0]=='templates':
            print "Task template directory :", taskdefdir
            print
            print "Available task templates :"
            print
            tc = filter(lambda x: x.endswith('_task'), task_registry.keys())
            for t in tc:
                print " *", t[:-5]
                for l in task_registry[t].doc:
                    print "   ", l

                print

    if len(args)==2:
        if args[0]=='files':
            read_hackide(open(args[1]).xreadlines())
            print '\n'.join(sorted((rc.path for rc in all_rc.values())))

    return 0





if __name__=='__main__':
    sys.exit(main(sys.argv[2:]))
