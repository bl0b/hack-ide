import os, sys

from base import *
from tmux import *
from rc_file import *

__all__ = [ 'all_tasks', 'all_embedded', 'get_task_prefix', 'push_task_prefix', 'pop_task_prefix', 'create_task', 'create_task_class', 'task_registry', 'rc_file', 'user_dir_tasks', 'site_dir_tasks' ]

task_prefix = ""

get_task_prefix = lambda: task_prefix

def push_task_prefix(v):
    global task_prefix
    task_prefix = task_prefix and '%s_%s_'%(task_prefix, v) or v+'_'
    return task_prefix

def pop_task_prefix():
    global task_prefix
    task_prefix = '_'.join(task_prefix.split('_')[:-2])
    if task_prefix:
        task_prefix += '_'
    return task_prefix


all_tasks = {}

all_embedded = {}

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
        self.doc = "This task template has no doc for it's the base class, and not meant to be used directly."
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
        self.opts = "UNSET"
        self.parent = None
        self.split_opts = ""
    def __str__(self):
        return self['T']+'(#%i p=%s o=%s)'%(self.task_index, str(self.parent and self.parent.task_index), str(self.opts))
    def __repr__(self):
        return self['T']+'(#%i p=%s o=%s)'%(self.task_index, str(self.parent and self.parent.task_index), str(self.opts))
    def tmux_shell_cmd(self):
        #return "printf '\033]2;%s\033\\' ; echo 'pane:%i\ntask:%i\nparent:%s\n'; cd %s ; while true; do %s; done"%(self['T'], self.pane_index, self.task_index, str(self.parent and self.parent.task_index), self.cmd_wd, self.parse(self.cmd_template))
        return "printf '\033]2;%s\033\\' ; cd %s ; while true; do %s; done"%(self['T'], self.cmd_wd, self.parse(self.cmd_template))
    def tmux_cmd(self):
        if self.parent is None:
            return tmux_window(self.tmux_shell_cmd())
        else:
            return tmux_split(self.parent, self.split_opts)


def create_task(t):
    name, rmember = [x.strip() for x in t.split(" => ")]
    if task_prefix!="":
        name = task_prefix+name
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
    doc = []
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
        elif l=='DOC':
            output = lambda v: doc.append(v)
            end_marker = "END DOC"
    #print "task has cmd template", CMD
    #print "task has RC files", rc_files

    def init_wrapper(self, contextname, taskname, param):
        param = param.strip()
        x = param.find(' ')
        if x==-1:
            wd = param
            par = ""
        else:
            wd = param[:x]
            par = param[x+1:]
        task.__init__(self, contextname, taskname, par)
        self.cmd_wd = wd
        self['PARAM'] = par
        for k in rc_files:
            ft, cts = rc_files[k]
            fn = self.parse(ft)
            cts = self.parse('\n'.join(cts))
            self[k] = rc_file(fn, cts).path

        self.cmd_template = self.parse(CMD)

    return type(clsname, (task,), { '__init__':init_wrapper, 'doc':doc })



# static module init

site_dir_tasks = hackide_root+'/tasks'
user_dir_tasks = os.getenv('HOME')+'/.hackide/tasks'
os.path.isdir(user_dir_tasks) or os.makedirs(user_dir_tasks)
for taskdefdir in (site_dir_tasks, user_dir_tasks):
    for task_def in os.listdir(taskdefdir):
        if not task_def.endswith('.task'):
            continue
        create_task_class(taskdefdir+'/'+task_def)

