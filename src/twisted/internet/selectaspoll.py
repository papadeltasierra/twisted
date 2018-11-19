# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
UNIX selectasepoll.

Maintainer: Itamar Shtull-Trauring
"""
from select import poll, POLLIN, POLLPRI, POLLOUT, POLLERR


def _select(rlist, wlist, xlist, timeout=-1):
    """
    Emulation of the select.select interface based on select.poll instead
    to avoid the 'file descriptors > 1023' issue on later versions of Linux.
    """
    poller = poll()

    # Create combined list with no duplicates
    fds = set(rlist + wlist + xlist)
    for fd in fds:
        event = 0
        if fd in rlist:
            event |= (POLLIN | POLLPRI)
        if fd in wlist:
            event |= POLLOUT
        if fd in xlist:
            event |= POLLERR

    poller.register(fd, event)
    events = poller.poll(timeout=0)

    rlist = []
    wlist = []
    errors = []
    for fd, event in events:
        if event & (POLLIN | POLLPRI):
            rlist.append(fd)
        if event & POLLOUT:
            wlist.append(fd)
        if event & POLLERR:
            errors.append(fd)

    return(rlist, wlist, xlist)
