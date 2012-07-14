import os
import time
import random
import pickle
import threading
import queue
from Song import Song

lib_config = {
    'path': ['/home/piplup/music'],
    'playable_ext': ['.mp3', '.aac', '.mp4', '.flac'],
    'bad_ext': ['db'],
    'del_ext': ['del'],
    'history_path': '/home/piplup/music/history.dat'
    }

"""
Lazily scans library and adds hash value for song. 
This way the app is more responsive cuz hashing 100k files
will take some time.
"""
class HasherDaemon:
  def __init__(self, lib):
    self.hash_q = queue.Queue()
    self.hasher = threading.Thread(
        target=HasherDaemon.start, 
        name="Hasher Daemon", 
        args=(self.hash_q,lib,))
    self.hasher.daemon = True
    self.hasher.start()

    for i in lib.song_list:
      if i.missing_hash:
        self.hash_q.put(i)

  def start(q, lib):
    while (True):
      time.sleep(0.2)
      song = q.get()
      lib.acquire()
      try:
        song.hash()
      except Exception as inst:
        print(inst)
      lib.release()


"""
Organizes music and gives out random songs.
"""
class Library:

  def __init__(self):
    random.seed()
    self.song_list = Library.load()
    self.lock = threading.Lock()
    self.hasher = HasherDaemon(self)

  def rand(self):
    lib.acquire()
    ''' Return a random song '''
    copy = Song(self.song_list[random.randint(0, len(self.song_list)-1)])
    lib.release()
    return copy

  @staticmethod
  def load():
    try:
      f = open(lib_config['history_path'], 'rb')
      song_list = pickle.load(f)
      f.close()
      return song_list
    except:
      print("rehash")
      return Library.rehash()

  @staticmethod
  def save(lib, path=lib_config['history_path']):
    lib.acquire()
    f = open(path, 'wb')
    pickle.dump(lib.song_list, f, pickle.HIGHEST_PROTOCOL)
    f.close()
    lib.release()

  @staticmethod
  def rehash(path_list = lib_config['path'], 
             playable_ext = lib_config['playable_ext']):
    s = []
    for path in path_list:
      for root, dirs, files in os.walk(path, followlinks=True):
        for name in files:
          if os.path.splitext(name)[1] in playable_ext:
            s.append(Song(os.path.join(root, name)))
    if not s:
      raise "No music found."
    return s


  def acquire(self):
    self.lock.acquire();

  def release(self):
    self.lock.release();


if __name__ == '__main__':
  a = Library()
  print(a.rand())
