import os, sys

from base import *
from task import *
from tmux import *

__all__ = [ 'create_layout', 'layout2tmux' ]
#DEBUG ONLY
__all__ += [ 'layout', 'reg_order' ]


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
        return T_SYM, get_task_prefix()+txt[:i], txt[i:]
    while ord('0') <= ord(txt[i]) <= ord('9'):
        i=i+1
    if i>0:
        return T_NUM, txt[:i], txt[i:]
    raise Exception("Scan failed around '%s'"%txt)


def make_pane(v):
    if v in all_embedded:
        return subcontext(all_embedded[v]['layout'])
    else:
        return pane(v)

def accept(tok, toktype):
    t, v = tok
    if t is not toktype:
        raise ValueError(t)

def parse_layout(tokiter):
    t, v = tokiter.next()
    if t is T_OPEN:
        left = parse_layout(tokiter)
    elif t is T_SYM:
        left = make_pane(v)
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
        right = make_pane(v)
    else:
        raise ValueError(t)
    accept(tokiter.next(), T_CLOSE)
    return splitter(mode, sz, left, right)


class pane(object):
    def __init__(self, name):
        self.name = name
        self.task = all_tasks[name]
        self.index = -1
        self.opts = None
#    def set_index(self):
#        pass
    def first_pane(self):
        return self
    def __str__(self):
        return self.task['T']
    def __repr__(self):
        return self.task['T']

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
#    def set_index(self):
#        self.a.index = self.index
#        self.b.index = splitter.alloc_index()
#        self.a.set_index()
#        self.b.set_index()
    def first_pane(self):
        return self.a.first_pane()
    def flat_pane_list(self, parent=None, parent_opts = None):
        l = []
        if type(self.a) in (splitter, subcontext):
            l += self.a.flat_pane_list(parent, parent_opts)
        else:
            l += [ (self.a.index, parent, parent_opts, self.a.task.tmux_shell_cmd()) ]
        if type(self.b) in (splitter, subcontext):
            l += self.b.flat_pane_list(self.a.index, self.opts)
        else:
            l += [ (self.a.index, self.index, self.opts, self.b.task.tmux_shell_cmd()) ]

        return sorted(l, None, lambda x: x[0])

    def __str__(self):
        if self.opts.startswith("-v"):
            sep = "--"+self.opts[6:]
        else:
            sep = "|"+self.opts[6:]
        return "(%s %s %s)"%(str(self.a), sep, str(self.b))
    def __repr__(self):
        return str(self)

class subcontext(splitter):
    def __init__(self, l):
        print l, l.opts
        mode, t, sz = l.opts.split(' ')
        splitter.__init__(self, mode, ' '.join((t, sz)), l.a, l.b)

layout = None


def pane2cmd(x, p, opts):
    if x.index==-1:
        x.index = splitter.alloc_index()
    return [(p and p.index, opts, x.task)]



def reg_order(l):
    def reg_if_new(x, v, p, opts):
        if x.task.task_index!=-1:
            return
        x.index = v()
        x.task.task_index = x.index
        x.task.opts = opts
        x.task.parent = p
    def rec_reg(l):
        if type(l) in (splitter, subcontext):
            fp = l.first_pane()
            sp = l.b.first_pane()
            reg_if_new(fp, splitter.alloc_index, None, None)
            l.index = fp.task.pane_index
            reg_if_new(sp, splitter.alloc_index, fp.task, l.opts)
            rec_reg(l.a)
            rec_reg(l.b)
    def pane_order(l):
        first = l.first_pane()
        L = []
        def rec(l):
            print "rec", l
            if type(l) is pane:
                L.append(l)
            elif type(l) in (splitter, subcontext):
                rec(l.a)
                rec(l.b)
        rec(l)
        print len(L), L, len(all_tasks)
        for i in xrange(len(L)):
            L[i].pane_index = i
        return L
    for x in all_tasks.values():
        x.task_index = -1
        x.pane_index = -1
    splitter.top_index=-1
    print pane_order(l)
    rec_reg(l)


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
    #accept(tokiter.next(), T_OPEN)
    t, v = tokiter.next()
    if t is T_OPEN:
        layout = parse_layout(tokiter)
    elif t is T_SYM:
        layout = make_pane(v)
    reg_order(layout)
    return layout

def layout2tmux():
    L = sorted((t for t in all_tasks.values() if t.task_index!=-1), None, lambda x: x.task_index)
    print L
    #return [ tmux_window(L[0].tmux_shell_cmd()) ] + [ tmux_split(l.parent.pane_index, l.opts, l.tmux_shell_cmd()) for l in L[1:] ]
    return [ tmux_window(L[0].tmux_shell_cmd()) ] + [ tmux_split(l.parent.task_index, l.opts, l.tmux_shell_cmd()) for l in L[1:] ]

