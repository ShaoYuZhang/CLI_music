"""
Configured UserInterface.. 
Uses print or curses  
cuz.. curses too difficult to use.
"""

class UserInterface:

  def __init__(self, scr=None):
    self.scr = scr

  def putCommandLine(self, update):
    if self.scr:
      pass
    else:
      print(update)

  def putDebug(self, update):
    if self.scr:
      pass
    else:
      print(update)

  def pplayer(self, update):
    if self.scr:
      pass
    else:
      print(update)
