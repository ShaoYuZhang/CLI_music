import re
import functools
#ha = functools.partial(pll.play, "/tmp/haha.mp3")

oneoff = ['a']

matcher = [
    (re.compile('^a$'), functools.partial(print, 'haha')) 
    ]

def match(cmdline):
  for m in matcher:
    s = m[0].match(cmdline)
    if s:
      return m[1]
  return None
