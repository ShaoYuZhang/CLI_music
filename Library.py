import os
import random

lib_config = {
    'path': ['/home/piplip/music'],
    'playable_ext': ['mp3', 'aac', 'mp4', 'flac'],
    'bad_ext': ['db'],
    'del_ext': ['del'],

    }

class Library:
  def __init__(self, path_list):
    random.seed()
    s = []
    for path in path_list:
      for root, dirs, files in os.walk(path):
        for name in files:
          s.append(os.path.join(root, name))

    self.file_list = s

  def rand(self):
    ''' Return a random song '''
    return self.file_list[random.randint(0, len(self.file_list)-1)]

if __name__ == '__main__':
  a = Library(['/home/piplup/programming'])
  print(a.rand())
