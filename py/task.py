import os, sys

from base import *
from tmux import *
from rc_file import *


all_tasks = {}

task_registry = {}


class template(dict):
    def __init__(*args):
        dict.__init__(*args)
    def parse(self, txt):
        #print "txt", txt
        #print "dict", self
        if not txt:
            return ''
        parse_one = lambda txt, k, v: v.join(txt.split(k))
        for k in self:
            #print k, self[k]
            txt = parse_one(txt, '%'+k+'%', self[k])
        #print "result", txt
        return txt

class task_metaclass(type):
    def __init__(cls, name, bases, dic):
        task_registry[name] = cls
        type.__init__(cls, name, bases, dic)

class task(template):
    __metaclass__ = task_metaclass
    def __init__(self, contextname, taskname, param):
        task_params = taskname.split(',')
        taskname = task_params[0]
        template.__init__(self)
        for p in task_params[1:]:
            words = p.split(':')
            if words[0]=='rc':
                self[words[1]] = rc_file(words[2]).path
        if taskname in all_tasks:
            raise NameError("Task "+taskname+" is already defined!")
        all_tasks[taskname] = self
        self['P'] = contextname
        self['T'] = taskname
        self['RC'] = ide_data_path
        self.task_index = len(all_tasks)
        self.pane_index = -1
        self.parent = None
        self.split_opts = ""
    def tmux_shell_cmd(self):
        return "printf '\033]2;%s\033\\' ; cd %s ; while true; do %s; done"%(self['T'], self.cmd_wd, self.parse(self.cmd_template))
    def tmux_cmd(self):
        if self.parent is None:
            return tmux_window(self.tmux_shell_cmd())
        else:
            return tmux_split(self.parent, self.split_opts)


def create_task(t):
    name, rmember = [x.strip() for x in t.split(" => ")]
    i = rmember.find(" ")
    tasktype = i!=-1 and rmember[:i] or rmember
    param = i!=-1 and rmember[i+1:] or ""
    return task_registry[tasktype+'_task'](get_context_name(), name, param)

def create_task_class(descfilename):
    #print "creating task template from", descfilename
    clsname = os.path.basename(descfilename)[:-5]+'_task'
    #print "task class has name", clsname
    desc = map(str.strip, open(descfilename).xreadlines())
    CMD = None
    output = lambda v: None
    rc_files = {}
    end_marker = None
    for l in desc:
        if end_marker is not None:
            if l==end_marker:
                output = lambda v: None
                end_marker = None
            else:
                output(l)
            continue
        if l.startswith("RC "):
            #print l
            #print l[3:]
            key, filenametemplate, cts = l[3:].split(' ')
            rc_files[key] = ( filenametemplate, [] )
            if cts=='CONTENTS':
                output = lambda v: rc_files[key][1].append(l)
                end_marker = "END "+key+" CONTENTS"
        elif l == end_marker:
            output = lambda v: None
            end_marker = None
        elif l.startswith('CMD '):
            CMD = l[4:]
    #print "task has cmd template", CMD
    #print "task has RC files", rc_files

    def init_wrapper(self, contextname, taskname, param):
        x = param.split(' ')
        wd, par = x[0] or '.', '\n'.join(x[1:])
        task.__init__(self, contextname, taskname, par)
        self.cmd_wd = wd
        self['PARAM'] = par
        for k in rc_files:
            ft, cts = rc_files[k]
            fn = self.parse(ft)
            cts = self.parse('\n'.join(cts))
            self[k] = rc_file(fn, cts and '\n'.join(cts) or '').path
        self.cmd_template = self.parse(CMD)
    return type(clsname, (task,), { '__init__':init_wrapper })

