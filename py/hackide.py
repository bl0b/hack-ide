import os, sys, re

from base import *
from task import *
from task import template
from rc_file import all_rc
from layout import create_layout

__all__ = [ 'read_hackide' ]


def embed_hackide(l):
    words = l.split(' ')
    name = words[0]
    prefix = words[1]
    t = template(zip((str(x) for x in xrange(1, len(words)-1)), words[2:]))
    t['prefix'] = push_task_prefix(prefix)
    lines = ( t.parse(l) for l in open(name).xreadlines() )
    all_embedded[prefix] = read_hackide(lines)
    pop_task_prefix()
    return all_embedded[prefix]



processors = {
    'context': set_context_name,
    'task': create_task,
    'embed': embed_hackide,
    'layout': create_layout,
}






_inside_read_hackide = 0

def read_hackide(lines):
    global _inside_read_hackide
    ret = {}
    #print "entering read_hackide", _inside_read_hackide
    if 0==_inside_read_hackide:
        all_rc.clear()
        all_tasks.clear()
    #else:
        #print 'all_rc', all_rc
        #print 'all_tasks', all_tasks
    _inside_read_hackide += 1
    for l in (l.strip() for l in lines):
        if len(l)==0 or l.startswith("#"):
            continue
        #print "reading line", l
        wlim = l.find(" ")
        if wlim!=-1:
            w = l[:wlim]
            ret[w] = processors[w](l[wlim+1:])
            #print w, ret[w]
        else:
            w = l
            ret[w] = processors[w](l)
    _inside_read_hackide -= 1
    #print "exiting read_hackide", _inside_read_hackide
    return ret

