import queue
import threading
import queue
from MPlayer import *

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

  def __init__(self):
    MPlayer.populate()
    self.mp = MPlayer()
    self.alarm_q = queue.Queue()
    self.cancel_alarm = threading.Event()
    self.reminder = threading.Thread(target=Alarm, args=(self.alarm_q,))
    self.reminder.daemon = True
    self.reminder.start()

  def play(self, path):
    self.quit()
    self.mp = MPlayer()
    self.mp.loadfile('"' + path + '"');
    length = float(self.mp.get_property("length"))
    print((self.quit, self.cancel_alarm, length))
    self.alarm_q.put((self.quit, self.cancel_alarm, length))

  def play_next(self):
    self.mp = MPlayer()
    self.mp.loadfile('"' + path + '"');

  def quit(self):
    self.cancel_alarm.set() # Don't need alarm.
    self.mp.quit()


