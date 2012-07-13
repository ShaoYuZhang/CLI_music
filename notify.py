"""
Notify using libnotify
"""
import subprocess
import pynotify

class Notifier:
  def __init__(self):
    pynotify.init("PyPly")

  def __call__(self, title, message):
    n = pynotify.Notification(title, message)
    n.show()

    #n.set_timeout(seconds)
    #n.set_urgency(pynotify.URGENCY_LOW)
    #n.set_urgency(pynotify.URGENCY_NORMAL)
    #n.set_urgency(pynotify.URGENCY_CRITICAL)
    #n.set_icon_from_pixbuf(icon)


if __name__ == '__main__':
  Notifier()("title", "messagE")
