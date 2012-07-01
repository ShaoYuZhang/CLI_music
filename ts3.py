import os
import sys
import time
import curses
import functools
import queue
import locale
import threading
from textpad import *
from Player import *
from CommandInterpreter import *

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

def debug(scr, s):
  numDebug = 20
  y,x = scr.getmaxyx()
  win = curses.newwin(1, x, 2, 1)


def start(scr):
  y,x = scr.getmaxyx()
  player = Player(curses.newwin(5, x, 0, 0))
  cmd2action = CmdToAction(player);

  try:
    t = threading.Thread(target=Player.go, args=(player.get_queue(),))
    t.daemon = True
    t.start()

    # play a song.
    win = curses.newwin(1, x, 0, 0)
    o = curses.newwin(4, x, 1, 0)
    while True:
      p = CommandLine(win)
      
      s = p.edit()

      o.addstr(s)
      o.refresh()

      action = cmd2action.match(s)
      if action:
        player.put(action)
  finally:
    player.put(player.quit)

if __name__ == '__main__':
  #start(None)

  s = curses.wrapper(start)
