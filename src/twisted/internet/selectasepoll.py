# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
UNIX selectasepoll.

Maintainer: Itamar Shtull-Trauring
"""
from select import epoll, EPOLLIN, EPOLLPRI, EPOLLOUT, EPOLLERR


def _select(rlist, wlist, xlist, timeout=-1):
    """
    Emulation of the select.select interface based on select.epoll instead
    to avoid the 'file descriptors > 1023' issue on later versions of Linux.
    """
    epoller = epoll()

    # Create combined list with no duplicates
    fds = set(rlist + wlist + xlist)
    for fd in fds:
        event = 0
        if fd in rlist:
            event |= (EPOLLIN | EPOLLPRI)
        if fd in wlist:
            event |= EPOLLOUT
        if fd in xlist:
            event |= EPOLLERR

    epoller.register(fd, event)
    events = epoller.poll(timeout=0)

    rlist = []
    wlist = []
    errors = []
    for fd, event in events:
        if event & (EPOLLIN | EPOLLPRI):
            rlist.append(fd)
        if event & EPOLLOUT:
            wlist.append(fd)
        if event & EPOLLERR:
            errors.append(fd)

    return(rlist, wlist, xlist)
