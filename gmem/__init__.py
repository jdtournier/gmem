#!/usr/bin/python

import sys, time
import plotext as plt
from operator import add

def run():
  kb2gb = 1/(1024**2)

  with open ('/proc/meminfo', 'r') as fd:
    for line in fd.readlines():
      kv = [ x.strip() for x in line.split () ]
      if kv[0] == 'MemTotal:':
        memtotal = kb2gb * int(kv[1])
        break

  plt.canvas_color ('default')
  plt.axes_color ('default')
  plt.ticks_color ('default')
  plt.ylabel('RAM (GB)')

  used = [ 0.0 ] * plt.terminal_width()
  buffers = used
  cached = buffers

  while True:
    with open ('/proc/meminfo', 'r') as fd:
      for line in fd.readlines():
        kv = [ x.strip() for x in line.split () ]
        if kv[0] == 'MemFree:': memfree = kb2gb * int(kv[1])
        elif kv[0] == 'Cached:': memcached = kb2gb * int(kv[1])
        elif kv[0] == 'Buffers:': membuffer = kb2gb * int(kv[1])
        elif kv[0] == 'SReclaimable:': memreclaim = kb2gb * int(kv[1])
        elif kv[0] == 'Shmem:': shmem = kb2gb * int(kv[1])

    # from https://stackoverflow.com/a/41251290
    buffers = buffers[1:] + [ membuffer ]
    memcached = memcached + memreclaim - shmem
    cached = cached[1:] + [ memcached ]
    used = used[1:] + [ memtotal - memfree - membuffer - memcached ]

    # for stacking:
    buffers[-1] += used[-1]
    cached[-1] += buffers[-1]

    plt.clear_data()
    plt.plot (cached, label='cached', color='orange')
    plt.plot (buffers, label='buffers', color='blue')
    plt.plot (used, label='used', color='red')
    plt.ylim (0, memtotal)
    plt.clear_terminal()
    plt.show()

    time.sleep (0.1)

