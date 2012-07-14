#!/usr/bin/python3

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
from ui import UserInterface

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()


def start(scr=None):
  ui = UserInterface(scr)
  player = Player(ui)
  cmd2action = CmdToAction(player);

  try:
    while True:
      if scr:
        p = CommandLine(ui)
        s = p.edit()
      else:
        s = input();

      action = cmd2action.match(s)
      if action:
        player.put(action)
  except:
    pass
  finally:
    player.quit()


if __name__ == '__main__':
  start(None)
  #s = curses.wrapper(start)
