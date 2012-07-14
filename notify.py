"""
Notify using libnotify
"""
import subprocess

class Notifier:
  def __call__(self, title, message =''):
    subprocess.call(["notify-send", title, message])

if __name__ == '__main__':
  Notifier()("title", "messagE")
  Notifier()("title")
