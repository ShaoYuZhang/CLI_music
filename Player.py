import queue
import threading
import queue
from MPlayer import *
from Library import *

def Alarm(q):
  while (True):
    (timeout_action, event, timeout) = q.get()
    wokeup = event.wait(timeout)
    if not wokeup:
      timeout_action();


class Player:
  @staticmethod
  def go(q):
    while (True):
      item = q.get()
      item()
      q.task_done()

  def __init__(self, scr):
    MPlayer.populate()
    self.scr = scr
    self.lib = Library()
    self.mp = MPlayer()
    self.alarm_q = queue.Queue()
    self.cancel_alarm = threading.Event()
    self.reminder = threading.Thread(target=Alarm, args=(self.alarm_q,))
    self.reminder.daemon = True
    self.reminder.start()
    self.player_q = queue.Queue()

  def get_queue(self):
    return self.player_q

  def play(self, path):
    self.quit()
    self.mp = MPlayer()
    self.mp.loadfile('"' + path + '"');
    length = float(self.mp.get_property("length"))
    print((self.quit, self.cancel_alarm, length))
    self.alarm_q.put((self.next, self.cancel_alarm, length))

  def next(self):
    self.mp = MPlayer()
    f = self.lib.rand()
    self.scr.addstr('next'+f)
    self.scr.refresh()
    self.mp.loadfile(f);
    length = float(self.mp.get_property("length"))
    self.alarm_q.put((self.next, self.cancel_alarm, length))

  def pause(self):
    self.mp.pause()

  def quit(self):
    self.cancel_alarm.set() # Don't need alarm.
    self.mp.quit()

  def put(self, action):
    self.player_q.put(action)
