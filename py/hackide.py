import os, sys, re, shlex

from base import *
from task import *
from task import template
from rc_file import all_rc
from layout import *

__all__ = [ 'read_hackide', 'embed_hackide' ]


def embed_hackide(l):
    if type(l) is str:
        words = shlex.split(l)
    else:
        words = l
    name = words[0]
    prefix = words[1]
    t = template(zip((str(x) for x in xrange(1, len(words)-1)), words[2:]))
    t['prefix'] = push_task_prefix(prefix)
    if name in all_context_templates:
        src = all_context_templates[name]
    else:
        src = open(name).xreadlines()
    lines = ( t.parse(l) for l in src )
    all_embedded[prefix] = read_hackide(lines)
    pop_task_prefix()
    return all_embedded[prefix]



def propagate_doc_and_tmux(hi, sub):
    hi['tmux'] += sub['tmux']
    hi['doc'] += ['', 'See also documentation for embedded context '+sub['context']]


processors = {
    'context': (lambda l: _inside_read_hackide>1 and get_context_name() or set_context_name(l), None),
    'task': (create_task, None),
    'embed': (embed_hackide, propagate_doc_and_tmux),
    'layout': (create_layout, None),
    'window': (create_window, None),
}






_inside_read_hackide = 0

def read_hackide(lines):
    global _inside_read_hackide
    ret = { 'doc': [], 'tmux':[] }
    #print "entering read_hackide", _inside_read_hackide
    if 0==_inside_read_hackide:
        all_rc.clear()
        all_tasks.clear()
        all_windows.clear()
    #else:
        #print 'all_rc', all_rc
        #print 'all_tasks', all_tasks
    _inside_read_hackide += 1
    output = None
    for l in (l.strip() for l in lines):
        if len(l)==0 or l.startswith("#"):
            continue
        print "[hack-ide] reading line", l
        if l=='DOC':
            output = lambda x: ret['doc'].append(x)
            continue
        elif l=='END DOC':
            output = None
            continue
        elif l=='TMUX':
            output = lambda x: ret['tmux'].append(x)
            continue
        elif l=='END TMUD':
            output = None
            continue
        elif output is not None:
            output(l)
            continue
        # All other lines are single-line entries, where the first word defines the entry type.
        wlim = l.find(" ")
        if wlim!=-1:
            w = l[:wlim]
            proc, postproc = processors[w]
            ret[w] = proc(l[wlim+1:])
            if postproc:
                postproc(ret, ret[w])
            #print w, ret[w]
        else:
            w = l
            ret[w] = processors[w](l)
    _inside_read_hackide -= 1
    #print "exiting read_hackide", _inside_read_hackide
    return ret

