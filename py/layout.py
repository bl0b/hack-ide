import os, sys

from base import *
from task import *

__all__ = [ 'create_layout' ]


T_OPEN = '('
T_CLOSE = ')'
T_SYM = 'sym'
T_VERT = '|'
T_HORIZ = '--'
T_ERROR = '!'
T_NUM = '0'

sym_alphabet = set()
num_alphabet = set()
for c in xrange(ord('a'), ord('z')+1):
    sym_alphabet.add(c)
for c in xrange(ord('A'), ord('Z')+1):
    sym_alphabet.add(c)
for c in xrange(ord('0'), ord('9')+1):
    sym_alphabet.add(c)
    num_alphabet.add(c)
sym_alphabet.add(ord('_'))
sym_alphabet.add(ord('-'))

def layout_scanner(txt):
    txt = txt.lstrip()
    if txt.startswith(T_OPEN):
        return T_OPEN, '', txt[len(T_OPEN):]
    if txt.startswith(T_CLOSE):
        return T_CLOSE, '', txt[len(T_CLOSE):]
    if txt.startswith(T_VERT):
        return T_VERT, '', txt[len(T_VERT):]
    if txt.startswith(T_HORIZ):
        return T_HORIZ, '', txt[len(T_HORIZ):]
    i=0
    while ord(txt[i]) in num_alphabet:
        i=i+1
    if i>0:
        return T_NUM, txt[:i], txt[i:]
    while ord(txt[i]) in sym_alphabet:
        i=i+1
    if i>0:
        return T_SYM, txt[:i], txt[i:]
    while ord('0') <= ord(txt[i]) <= ord('9'):
        i=i+1
    if i>0:
        return T_NUM, txt[:i], txt[i:]
    raise Exception("Scan failed around '%s'"%txt)



def accept(tok, toktype):
    t, v = tok
    if t is not toktype:
        raise ValueError(t)

def parse_layout(tokiter):
    t, v = tokiter.next()
    if t is T_OPEN:
        left = parse_layout(tokiter)
    elif t is T_SYM:
        left = pane(v)
    else:
        raise ValueError(t)
    t, v = tokiter.next()
    if t is T_HORIZ:
        mode='-v'
    elif t is T_VERT:
        mode='-h'
    else:
        raise ValueError(t)
    t, v = tokiter.next()
    if t is not T_NUM:
        raise ValueError(t)
    sz = "-p "+v
    t, v = tokiter.next()
    if t is T_OPEN:
        right = parse_layout(tokiter)
    elif t is T_SYM:
        right = pane(v)
    else:
        raise ValueError(t)
    accept(tokiter.next(), T_CLOSE)
    return splitter(mode, sz, left, right)


class pane(object):
    def __init__(self, name):
        self.name = name
        self.task = all_tasks[name]
        self.index = -1
#    def tmux_cmds(self):
#        p=self.task['P']
#        t=self.task['T']
#        return [
#            'new-window -n %s -t %s:%i "%s"'%(self.task['T'], self.task['P'], self.task.task_index, self.task.tmux_shell_cmd()),
#            'swap-pane -s %s:%s.0 -t %s:hack-ide.%i'%(p, t, p, self.index),
#            'kill-window -t %s:%i'%(self.task['P'], self.task.task_index)
#        ]
    def set_index(self):
        pass
    def first_pane(self):
        return self

class splitter(object):
    top_index = 0
    @classmethod
    def alloc_index(cls):
        cls.top_index += 1
        return cls.top_index
    def __init__(self, mode, sz, a, b):
        self.opts = mode+" "+sz
        self.a = a
        self.b = b
        self.index = 0
    def set_index(self):
        self.a.index = self.index
        self.b.index = splitter.alloc_index()
        self.a.set_index()
        self.b.set_index()
    def first_pane(self):
        return self.a.first_pane()
    def flat_pane_list(self, parent=None, parent_opts = None):
        l = []
        if type(self.a) is splitter:
            l += self.a.flat_pane_list(parent, parent_opts)
        else:
            l += [ (self.a.index, parent, parent_opts, self.a.task.tmux_shell_cmd()) ]
        if type(self.b) is splitter:
            l += self.b.flat_pane_list(self.a.index, self.opts)
        else:
            l += [ (self.a.index, self.index, self.opts, self.b.task.tmux_shell_cmd()) ]

        return sorted(l, None, lambda x: x[0])


layout = None

def create_layout(l):
    global layout
    tokens = []
    splitter.top_index=0
    try:
        while len(l)>0:
            t, v, l = layout_scanner(l)
            tokens.append((t, v))
    except Exception, e:
        print e
        pass
    #print tokens
    tokiter = iter(tokens)
    accept(tokiter.next(), T_OPEN)
    layout = parse_layout(tokiter)
    layout.set_index()
    return map(lambda x: x[1] is None and tmux_window(x[3]) or tmux_split(*x[1:]), layout.flat_pane_list())

