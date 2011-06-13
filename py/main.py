#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

from base import *
from tmux import *
from task import *
from hackide import *
from layout import *
from rc_file import *

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
    #print 'DEBUG', hi
    #print 'DEBUG', hi['layout']
    rc = '-f %s '%tmuxrc
    ret = []
    try:
        session_exists = tmux('has-session -t '+hi['context'])[1]==0
    except ValueError, ve:
        session_exists = False
    if session_exists:
        print "[Reattaching to existing session %s]"%hi['context']
        try:
            ret = [ tmux('attach -t %s'%hi['context']) ]
        except ValueError, ve:
            print "An error occurred while sending command", ve.message
            return []
    else:
        print "[Spawning new session %s]"%hi['context']
        lcmd = layout2tmux()

        defensive_layout = lcmd[:1] # don't check for session before the new-session :)
        defensive_layout += map(lambda b: 'has-session -t '+get_context_name()+" ';' "+b, lcmd[1:])

        all_cmds = [ 'start-server' ]
        all_cmds += defensive_layout
        all_cmds += open(tmuxrc).xreadlines()
        all_cmds += hi['tmux']
        all_cmds += [ 'select-window -t %s:%s'%(get_context_name(), app_name), 'select-pane -t %s:%s.0'%(get_context_name(), app_name), 'attach -t %s'%(get_context_name()) ]

        ret = []
        try:
            for c in all_cmds:
                ret.append(tmux(c))
        except ValueError, ve:
            if ve.message == all_cmds[-1]:
                try:
                    print "[Killing session %s]"%get_context_name()
                    tmux('kill-session -t '+get_context_name())
                except ValueError, ve:
                    pass
                return ret
            print "An error occurred while creating session"
            print ve
            return ret

    return ret


def main(args):
    #tmuxrc = rc_file('tmuxrc', open(hackide_root+'/default.tmuxrc').read()).path
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
            print "Task template directories :"
            print site_dir_tasks
            print user_dir_tasks
            print
            print "Available task templates :"
            print
            tc = filter(lambda x: x.endswith('_task'), task_registry.keys())
            for t in tc:
                print " *", t[:-5]
                for l in task_registry[t].doc:
                    print "   ", l

                print
    elif args[0] == 'test-layout':
        set_task_cmd_dummy(True)
        return main(args[1:])
    elif args[0] in all_context_templates:
        respawn(embed_hackide(args), tmuxrc)

    if len(args)==2:
        if args[0]=='files':
            read_hackide(open(args[1]).xreadlines())
            print '\n'.join(sorted((rc.path for rc in all_rc.values())))

    return 0





if __name__=='__main__':
    sys.exit(main(sys.argv[2:]))
