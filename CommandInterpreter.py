import re
import functools
#ha = functools.partial(pll.play, "/tmp/haha.mp3")

oneoff = ['p', 'n', 'i', 'd']

matcher = [
    (re.compile('^n$'), lambda player: functools.partial(player.play, 'next')),
    (re.compile('^p$'), lambda player: functools.partial(player.pause)),
    (re.compile('^i$'), lambda player: functools.partial(player.next)),
    (re.compile('^d$'), lambda player: functools.partial(player.delete)), 
    ]

class CmdToAction:
  def __init__(self, player):
    self.player = player
    self.player_q = player.get_queue()

  def match(self, cmdline):
    if cmdline == 'q':
      raise "Want to quit" # not a good control flow use...

    for m in matcher:
      s = m[0].match(cmdline)
      if s:
        return m[1](self.player)
    return None
