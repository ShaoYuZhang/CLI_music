import os
import random

lib_config = {
    'path': ['/home/piplup/music'],
    'playable_ext': ['.mp3', '.aac', '.mp4', '.flac'],
    'bad_ext': ['db'],
    'del_ext': ['del'],

    }

class Library:
  def __init__(self, path_list=lib_config['path']):
    random.seed()
    s = []
    for path in path_list:
      for root, dirs, files in os.walk(path, followlinks=True):
        for name in files:
          if os.path.splitext(name)[1] in lib_config['playable_ext']:
            s.append(os.path.join(root, name))

    if not s:
      raise "No music found."
    self.file_list = s

  def rand(self):
    ''' Return a random song '''
    return '"{0}"'.format(self.file_list[random.randint(0, len(self.file_list)-1)])

if __name__ == '__main__':
  a = Library()
  print(a.rand())
