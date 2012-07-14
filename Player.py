import queue
import threading
from MPlayer import *
from Library import *
from notify import Notifier

class AlarmClock:
  def __init__(self):
    self.alarm_q = queue.Queue()
    self.cancel_alarm = threading.Event()
    self.reminder = threading.Thread(
        target=AlarmClock.start, 
        name="Player", 
        args=(self.alarm_q, self.cancel_alarm,))
    self.reminder.daemon = True
    self.reminder.start()

  def start(q, cancel_alarm):
    while (True):
      (timeout_action, timeout) = q.get()
      wokeup = cancel_alarm.wait(timeout)
      if not wokeup:
        timeout_action();

  def set(self, action_when_wokeup, duration):
    self.cancel_alarm.clear()
    self.alarm_q.put((action_when_wokeup, duration))

  def cancel(self):
    self.cancel_alarm.set()


class Player:
  def go(q):
    while (True):
      item = q.get()
      item()
      q.task_done()

  def __init__(self, ui):
    MPlayer.populate()

    # Handle actions asynchronously
    self.player_q = queue.Queue()
    t = threading.Thread(target=Player.go, args=(self.player_q,))
    t.daemon = True
    t.start()

    # rather static..
    self.ui = ui
    self.lib = Library()
    self.notifier = Notifier();
    self.alarm = AlarmClock()

    # Really stateful variables
    self.lastSong = None
    self.mp = None

  def get_queue(self):
    return self.player_q

  def play(self, path):
    pass

  def next(self):
    self.reset()

    self.mp = MPlayer()
    song = self.lib.rand()
    self.ui.pplayer('next'+song.path())
    self.mp.loadfile(song.path());
    self.lastSong = song
    try:
      length = float(self.mp.get_property("length"))
      self.alarm.set(self.next, length)
    except:
      self.ui.pplayer('No length found'+song.path())
      # default to 250s
      self.alarm.set(self.next, 250.0)

    self.notifier(song.name());

  def pause(self):
    self.mp.pause()

  def reset(self):
    self.alarm.cancel()
    if self.mp:
      self.mp.quit()

  def quit(self):
    self.reset()
    Library.save(self.lib)

  def put(self, action):
    self.player_q.put(action)

  def delete(self):
    if self.lastSong:
      self.lastSong.delete()
      self.next()
