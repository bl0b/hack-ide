import os, sys, re

from base import *
from task import create_task
from layout import create_layout

__all__ = [ 'read_hackide' ]

processors = {
    'context': set_context_name,
    'task': create_task,
    'layout': create_layout,
}







def read_hackide(f):
    if type(f) is str:
        f=open(f)
    ret = {}
    for l in (l for l in (l.strip() for l in f.xreadlines()) if len(l)>0 and not l.startswith("#")):
        #print "reading line", l
        wlim = l.index(" ")
        w = l[:wlim]
        ret[w] = processors[w](l[wlim+1:])
        print w, ret[w]
    return ret
