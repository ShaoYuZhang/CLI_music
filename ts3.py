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
import CommandInterpreter

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()
q = queue.Queue()

def debug(scr, s):
  numDebug = 20
  y,x = scr.getmaxyx()
  win = curses.newwin(1, x, 2, 1)


def start(scr):
  pll = Player()
  player_q = queue.Queue()
  try:
    #t = threading.Thread(target=Player.go, args=(player_q,))
    #t.daemon = True
    #t.start()

    # play a song.
    #y,x = scr.getmaxyx()
    #win = curses.newwin(1, x, 0, 0)
    #p = CommandLine(win)
    #s = p.edit()
    #return s
    #ha = functools.partial(pll.play, "/tmp/haha.mp3")
    #player_q.put(ha)
    time.sleep(2000);
  finally:
    q.put(pll.quit)

if __name__ == '__main__':
  start(None)

  #s = curses.wrapper(start)
  #i = CommandInterpreter.match(s)
  #i()
